### flutter 安装教程

#### 安装flutter sdk

支持mac，windows，linux

1. 安装flutter sdk

   下载https://flutter.dev/docs/get-started/install/macos, 找个喜欢的位置解压

   ```
   # 路径随你算
   cd ~/flutter			
   unzip ~/Downloads/flutter_macos_2.2.3-stable.zip
   ```

   

   加入环境变量，让console能找到flutter

   ```
   # mac/linux: 路径加入环境变量~/.bash_prodfile
   export PATH="$PATH:~/flutter/bin"
   
   # windows环境
   右键“我的电脑”-->属性-->高级系统设置-->环境变量
   双击系统变量path，加入flutter/bin目录即可
   ```

   

   安装java

   ```
   http://www.java.com
   ```

   

   执行flutter doctor查看状态,能够正常输出内容，说明sdk安装完成

   ```
   # 执行flutter doctor
   Running "flutter pub get" in flutter_tools...                      16.7s
   Doctor summary (to see all details, run flutter doctor -v):
   [✓] Flutter (Channel stable, 2.2.3, on macOS 11.5.2 20G95 darwin-x64, locale
       en-CN)
   [✗] Android toolchain - develop for Android devices
       ✗ Unable to locate Android SDK.
         Install Android Studio from:
         https://developer.android.com/studio/index.html
         On first launch it will assist you in installing the Android SDK
         components.
         (or visit https://flutter.dev/docs/get-started/install/macos#android-setup
         for detailed instructions).
         If the Android SDK has been installed to a custom location, please use
         `flutter config --android-sdk` to update to that location.
   
   [✓] Xcode - develop for iOS and macOS
   [✓] Chrome - develop for the web
   [!] Android Studio (not installed)
   [✓] Connected device (1 available)
   ```

   

2. 确保java正常

   ```
   # java --verison
   java version "1.8.0_301"
   Java(TM) SE Runtime Environment (build 1.8.0_301-b09)
   Java HotSpot(TM) 64-Bit Server VM (build 25.301-b09, mixed mode)
   ```

   

3. (Mac)安装ios相关

   - mac安装xcode

   - 安装工具

   ```
    sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
    sudo xcodebuild -runFirstLaunch
   ```

   

4. 安装android相关

   安装android studio(含android sdk)：https://developer.android.com/studio?gclid=EAIaIQobChMItauhgsjk8gIVlIKRCh0ECwqwEAAYASAAEgKD_fD_BwE&gclsrc=aw.ds

   

   安装sdk command line tool

   https://stackoverflow.com/questions/61993738/flutter-doctor-android-licenses-gives-a-java-error

   ```
   打开android studio, 打开mac顶部菜单Preferences
   左侧菜单选择：Appearence & Behavior -> System Setting -> Android SDK
   右边窗口选择SDK Tools
   
   选中Android SDK Command-Line Tool, 点右下角确定开始安装
   ```

   

5. 检查fluter状态

   ```
   # flutter doctor
   Doctor summary (to see all details, run flutter doctor -v):
   [✓] Flutter (Channel stable, 2.2.3, on macOS 11.5.2 20G95 darwin-x64, locale en-CN)
   [!] Android toolchain - develop for Android devices (Android SDK version 31.0.0)
       ✗ Android licenses not accepted.  To resolve this, run: flutter doctor
         --android-licenses
   [✓] Xcode - develop for iOS and macOS
   [✓] Chrome - develop for the web
   [!] Android Studio (version 2020.3)
       ✗ Unable to find bundled Java version.
   [✓] Connected device (1 available)
   
   flutter doctor --android-licenses
   ```

   

   解决： Android licenses not accepted

   ```
   flutter doctor --android-licenses
   一路yes即可
   ```

   

   解决：Unable to find bundled Java version

   https://stackoverflow.com/questions/51281702/unable-to-find-bundled-java-version-on-flutter/68575967#68575967

   ```
   # cd /Applications/Android\ Studio.app/Contents/jre
   # ln -s ../jre jdk
   # ln -s "/Library/Internet Plug-Ins/JavaAppletPlugin.plugin" jdk
   
   # flutter doctor -v
   [✓] Flutter (Channel stable, 2.2.3, on macOS 11.5.2 20G95 darwin-x64, locale en-CN)
       • Flutter version 2.2.3 at /Users/yshi3/Desktop/flutter
       • Framework revision f4abaa0735 (9 weeks ago), 2021-07-01 12:46:11 -0700
       • Engine revision 241c87ad80
       • Dart version 2.13.4
   
   [!] Android toolchain - develop for Android devices (Android SDK version 31.0.0)
       • Android SDK at /Users/yshi3/Library/Android/sdk
       • Platform android-31, build-tools 31.0.0
       • Java binary at: /Applications/Android
         Studio.app/Contents/jre/jdk/Contents/Home/bin/java
       • Java version OpenJDK Runtime Environment (build 11.0.10+0-b96-7281165)
       ✗ Android license status unknown.
         Run `flutter doctor --android-licenses` to accept the SDK licenses.
         See https://flutter.dev/docs/get-started/install/macos#android-setup for more
         details.
   
   [✓] Xcode - develop for iOS and macOS
       • Xcode at /Applications/Xcode.app/Contents/Developer
       • Xcode 12.5.1, Build version 12E507
       • CocoaPods version 1.10.2
   
   [✓] Chrome - develop for the web
       • Chrome at /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
   
   [✓] Android Studio (version 2020.3)
       • Android Studio at /Applications/Android Studio.app/Contents
       • Flutter plugin can be installed from:
         🔨 https://plugins.jetbrains.com/plugin/9212-flutter
       • Dart plugin can be installed from:
         🔨 https://plugins.jetbrains.com/plugin/6351-dart
       • Java version OpenJDK Runtime Environment (build 11.0.10+0-b96-7281165)
   
   [✓] Connected device (1 available)
       • Chrome (web) • chrome • web-javascript • Google Chrome 93.0.4577.63
   ```

   

6. 安装成功

   ```
   # flutter doctor -v                
   [✓] Flutter (Channel stable, 2.2.3, on macOS 11.5.2 20G95 darwin-x64, locale en-CN)
       • Flutter version 2.2.3 at /Users/yshi3/Desktop/flutter
       • Framework revision f4abaa0735 (9 weeks ago), 2021-07-01 12:46:11 -0700
       • Engine revision 241c87ad80
       • Dart version 2.13.4
   
   [✓] Android toolchain - develop for Android devices (Android SDK version 31.0.0)
       • Android SDK at /Users/yshi3/Library/Android/sdk
       • Platform android-31, build-tools 31.0.0
       • Java binary at: /Applications/Android Studio.app/Contents/jre/jdk/Contents/Home/bin/java
       • Java version OpenJDK Runtime Environment (build 11.0.10+0-b96-7281165)
       • All Android licenses accepted.
   
   [✓] Xcode - develop for iOS and macOS
       • Xcode at /Applications/Xcode.app/Contents/Developer
       • Xcode 12.5.1, Build version 12E507
       • CocoaPods version 1.10.2
   
   [✓] Chrome - develop for the web
       • Chrome at /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
   
   [✓] Android Studio (version 2020.3)
       • Android Studio at /Applications/Android Studio.app/Contents
       • Flutter plugin can be installed from:
         🔨 https://plugins.jetbrains.com/plugin/9212-flutter
       • Dart plugin can be installed from:
         🔨 https://plugins.jetbrains.com/plugin/6351-dart
       • Java version OpenJDK Runtime Environment (build 11.0.10+0-b96-7281165)
   
   [✓] Connected device (1 available)
       • Chrome (web) • chrome • web-javascript • Google Chrome 93.0.4577.63
   
   • No issues found!
   ```




#### ide配置

配置IDE, 本文使用VSC

1. Start VS Code.
2. Invoke **View > Command Palette…**.
3. Type “install”, and select **Extensions: Install Extensions**.
4. Type “flutter” in the extensions search field, select **Flutter** in the list, and click **Install**. This also installs the required Dart plugin.



验证安装是否成功

1. Invoke **View > Command Palette…**.
2. Type “doctor”, and select the **Flutter: Run Flutter Doctor**.
3. Review the output in the **OUTPUT** pane for any issues. Make sure to select Flutter from the dropdown in the different Output Options.