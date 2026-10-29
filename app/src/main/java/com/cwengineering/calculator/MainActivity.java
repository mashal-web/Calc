package com.cwengineering.calculator;

import android.app.Activity;
import android.os.Bundle;
import android.os.Build;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebSettings;
import android.widget.FrameLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.LinearLayout;
import com.chaquo.python.PyException;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

public class MainActivity extends Activity {
    private WebView webView;
    private LinearLayout loading;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(Color.rgb(17, 24, 32));
        getWindow().setNavigationBarColor(Color.rgb(17, 24, 32));
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            getWindow().getAttributes().layoutInDisplayCutoutMode =
                android.view.WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
        }

        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(Color.rgb(17, 24, 32));
        webView = new WebView(this);
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient());
        root.addView(webView, new FrameLayout.LayoutParams(-1, -1));

        loading = new LinearLayout(this);
        loading.setOrientation(LinearLayout.VERTICAL);
        loading.setGravity(Gravity.CENTER);
        loading.setBackgroundColor(Color.rgb(17, 24, 32));
        ProgressBar spinner = new ProgressBar(this);
        loading.addView(spinner);
        TextView label = new TextView(this);
        label.setText("Starting CW Engineering…");
        label.setTextColor(Color.WHITE);
        label.setTextSize(16);
        label.setPadding(0, 20, 0, 0);
        loading.addView(label);
        root.addView(loading, new FrameLayout.LayoutParams(-1, -1));
        setContentView(root);

        new Thread(() -> {
            try {
                if (!Python.isStarted()) Python.start(new AndroidPlatform(this));
                Python.getInstance().getModule("app").callAttr("start_server");
                runOnUiThread(() -> {
                    loading.setVisibility(View.GONE);
                    webView.loadUrl("http://127.0.0.1:5000/");
                });
            } catch (Exception error) {
                runOnUiThread(() -> {
                    TextView message = new TextView(this);
                    message.setText("CW Engineering could not start.\n\n" + error.getMessage());
                    message.setTextColor(Color.WHITE);
                    message.setGravity(Gravity.CENTER);
                    message.setPadding(32, 32, 32, 32);
                    loading.removeAllViews();
                    loading.addView(message);
                    loading.setVisibility(View.VISIBLE);
                });
            }
        }, "CWStartup").start();
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }

    @Override
    protected void onDestroy() {
        if (webView != null) webView.destroy();
        super.onDestroy();
    }
}
