# CW Engineering — Android app project

This is an Android Studio/Gradle project wrapping the CW Engineering calculator UI in an Android WebView and running the existing Flask + SymPy engine inside the app with Chaquopy. The user does not need Termux or a separate server once an APK is built.

## Build an APK for free using GitHub Actions (phone-friendly)

1. Create a GitHub account if needed and create a **new empty repository** named `cw-engineering-android`.
2. Upload the *contents of this project folder* to the repository (not the ZIP itself). The `.github/workflows/build-apk.yml` file must be included. You can do this in GitHub's mobile website using **Add file → Upload files**; if GitHub mobile upload is awkward, use the repository's web interface in Chrome desktop-site mode.
3. Open the repository's **Actions** tab and select **Build CW Engineering APK**.
4. Tap **Run workflow**. Wait for the job to finish successfully.
5. Open the completed workflow run and download the artifact named `CW-Engineering-debug-apk`.
6. Extract the artifact ZIP, tap `app-debug.apk`, and allow installation from that source if Android asks.

Every build run uploads an APK artifact for 14 days. The artifact download is a ZIP containing the APK.

## Build locally

Open this folder in Android Studio with JDK 17 and Android SDK platform 35, then run `assembleDebug`.

## Important notes

- This is an **Android app project**, not a prebuilt APK. The APK is produced only after a successful build.
- This initial Android wrapper has not yet been compiled or tested on a physical phone in this environment. Confirm the GitHub Actions build succeeds before installing.
- Flask and SymPy are packaged through Chaquopy. First build can take several minutes and needs network access to download Gradle and Python dependencies.
- The calculator's local HTTP server listens only on `127.0.0.1` and is not exposed to the network.
- Engineering calculations should be independently checked before use in safety-critical decisions.
