### 让line框架支持基于key value的error message

效果，验证请求json参数，返回具体字段错误描述

```json
{
    "code":0,
    "errors":{
        "username":"username仅包含大小写字母和数字，长度6-32"
    },
    "message":"",
    "response":null,
    "xid":""
}
```



#### TODO

框架修改

1. line/http.go

```go
if bizErr, ok := err.(bizerr.BizLogicError); ok {
    httpCode = bizErr.HttpStatusCode()
    ret = map[string]interface{}{
        "code":     bizErr.ErrorNo(),
        "message":  bizErr.Message(),
        "errors":   bizErr.Errors(),		// 增加errors
        "xid":      rc.GetXid(),
        "response": ret,
    }
} else {
    httpCode = http.StatusInternalServerError
    ret = map[string]interface{}{
        "message":  err.Error(),
        "xid":      rc.GetXid(),
        "response": ret,
    }
}
```

2. line/bizerr/error.go

```go
type (
	BizLogicError interface {
		HttpStatusCode() int
		Message() string
		ErrorNo() int
		Errors() map[string]string		// 增加errors
		error
	}
	bizlogicError struct {
		httpCode int
		errorNo  int
		err      error
		errors   map[string]string		// 增加errors
	}
)

// 新增方法NewRequestErrors
func NewRequestErrors(errs map[string]string) BizLogicError {
    return bizlogicError{
        httpCode: http.StatusBadRequest,
        err:      errorx.New(""),
        errors:   errs,
    }
}

// 新增errors
func (be bizlogicError) Errors() map[string]string {
    return be.errors
}

```



请求参数验证代码

1. 新增common/feature/errcode/request.go

```go
package errcode

import (
	"fmt"
	"reflect"

	"github.com/go-playground/validator/v10"
)

var requestErrorMessage = map[string]string{
	"error_invalid_email":    "请输入一个有效地meail地址",
	"error_invalid_username": "username仅包含大小写字母和数字，长度6-32",
}

func GetErrorMessage(key string) string {
	if value, ok := requestErrorMessage[key]; ok {
		return value
	}
	return key
}

type ErrorResult struct {
	Field   string
	JsonTag string
	Message string
}

func ListOfErrors(model interface{}, err error) map[string]string {
	errors := map[string]string{}
	fields := map[string]ErrorResult{}

	//ErrorResult
	// resolve all json tags for the struct
	types := reflect.TypeOf(model)
	values := reflect.ValueOf(model)
	//val2 := val1.Elem()
	for i := 0; i < types.NumField(); i++ {
		field := types.Field(i)
		value := values.Field(i).Interface()
		jsonTag := field.Tag.Get("json")
		if jsonTag == "" {
			jsonTag = field.Name
		}
		messageTag := field.Tag.Get("msg")
		msg := GetErrorMessage(messageTag)

		fmt.Printf("%s: %v = %v, tag= %v\n", field.Name, field.Type, value, jsonTag)
		fields[field.Name] = ErrorResult{
			Field:   field.Name,
			JsonTag: jsonTag,
			Message: msg,
		}
	}

	//for err.Error()
	for _, e := range err.(validator.ValidationErrors) {
		fmt.Printf("error:\n")
		fmt.Printf("\ttag = %v\n", e.Tag())
		fmt.Printf("\terr = %v\n", e.Error())
		fmt.Printf("\tfield = %v\n", e.Field())
		fmt.Printf("\tvalue = %v\n", e.Value())
		fmt.Printf("\tstruct field = %v\n", e.StructField())
		fmt.Printf("\tparam = %v\n", e.Param())
		fmt.Printf("\tactual tag = %v\n", e.ActualTag())
		fmt.Printf("\tactual kind = %v\n", e.Kind())
		fmt.Printf("\tnamespace = %v\n", e.Namespace())
		fmt.Printf("\ttype = %v\n", e.Type())

		if field, ok := fields[e.Field()]; ok {
			if field.Message != "" {
				errors[field.JsonTag] = field.Message
			} else {
				errors[field.JsonTag] = e.Error()
			}
		}
	}

	return errors
}

```



2. 定义model，验证

```go
type RegisterForm struct {
	Email    string `json:"email" binding:"required,email" msg:"error_invalid_email"` // msg对应错误消息
	Username string `json:"username" binding:"required,alphanum,gte=6,lte=32" msg:"error_invalid_username"`
	Password string `json:"password" binding:"required,gte=6,lte=32"`
	Platform string `json:"platform" binding:"required"`
}


func (c Controller) Register(reqCtx appx.ReqContext) (interface{}, error) {
	req := model.RegisterForm{}
	if err := reqCtx.Gin().BindJSON(&req); err != nil {
		errors := errcode.ListOfErrors(req, err)
		return nil, bizerr.NewRequestErrors(errors)
	}
	return req, nil
}
```



