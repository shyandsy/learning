import 'package:flutter/material.dart';
import 'package:demo/store/appstate.dart';
import 'package:demo/model/cat.dart';

class DetailPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    //获取路由参数
    var args = ModalRoute.of(context)?.settings.arguments;
    String name = args.toString();
    Cat cat = AppState.catStore.getCatByName(name);

    return GestureDetector(
      behavior: HitTestBehavior.opaque,
      onDoubleTap: () => Navigator.of(context).pop(), // 双击页面
      child: Container(
        child: Center(
          child: Column(
            children: [
              Text("详细",
                  style: TextStyle(fontSize: 16, color: Colors.grey[800])),
              Image.asset(cat.image),
              Padding(
                padding: const EdgeInsets.only(left: 10.0),
              ),
              Text(cat.name,
                  style: TextStyle(fontSize: 16, color: Colors.grey[800])),
              Text(cat.description,
                  style: TextStyle(fontSize: 16, color: Colors.grey[800])),
            ],
          ),
        ),
      ),
    );
  }
}
