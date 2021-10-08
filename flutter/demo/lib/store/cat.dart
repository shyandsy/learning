import "package:demo/model/cat.dart";

class CatStore {
  List<Cat> cats = [];

  CatStore() {
    this.cats.add(Cat("美短", "assets/images/meiduan.jpg", "美国短毛猫"));
    this.cats.add(Cat("英短", "assets/images/yingduan.jpg", "英国短毛猫"));
  }

  getAllCats() {
    return this.cats;
  }

  getCatByName(String name) {
    return this.cats.firstWhere((cat) => cat.name == name);
  }
}
