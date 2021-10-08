import 'package:flutter/material.dart';
import 'package:demo/pages/home.dart';
import 'package:demo/pages/detail.dart';
import 'package:demo/pages/about.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // Try running your application with "flutter run". You'll see the
        // application has a blue toolbar. Then, without quitting the app, try
        // changing the primarySwatch below to Colors.green and then invoke
        // "hot reload" (press "r" in the console where you ran "flutter run",
        // or simply save your changes to "hot reload" in a Flutter IDE).
        // Notice that the counter didn't reset back to zero; the application
        // is not restarted.
        primarySwatch: Colors.blue,
      ),

      initialRoute: 'home', // 初始页面地址
      routes: <String, WidgetBuilder>{
        'home': (BuildContext context) =>
            MyHomePage(title: 'Flutter Demo Home Page'),
        'detail': (BuildContext context) => DetailPage(),
        'about': (BuildContext context) => new AboutPage(),
      },
    );
  }
}
