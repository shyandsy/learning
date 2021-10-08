import 'package:flutter/material.dart';
import 'package:demo/store/appstate.dart';
import 'package:demo/model/cat.dart';

class CatCardList extends StatelessWidget {
  final List<Cat> cats = AppState.catStore.getAllCats();
  final Widget seperateLine = Container(
    height: 1.5,
    color: Colors.grey,
  );

  Widget buildCatCard(BuildContext context, Cat cat) {
    return GestureDetector(
      onTap: () => {print("selected cat" + cat.name)}, // 单击事件处理
      child: Column(
        children: <Widget>[
          seperateLine,
          Container(
            color: Colors.white54, // .grey,
            padding: const EdgeInsets.only(
                top: 15.0, left: 20.0, right: 20.0, bottom: 15.0),
            child: Row(
              children: <Widget>[
                Expanded(
                  child: Column(
                    children: <Widget>[
                      Image.asset(cat.image),
                      Padding(
                        padding: const EdgeInsets.only(left: 10.0),
                      ),
                      Text(cat.name,
                          style:
                              TextStyle(fontSize: 16, color: Colors.grey[800])),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('模式选择'),
        centerTitle: true,
      ),
      body: new Container(
        decoration: new BoxDecoration(
          color: Colors.white,
          //image: new DecorationImage(
          //  image: new AssetImage("assets/images/bg.png"),
          //  fit: BoxFit.cover
          //),
        ),
        child: ListView(
            children: cats.map((cat) => buildCatCard(context, cat)).toList()),
      ),
    );
  }
}
