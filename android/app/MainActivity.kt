class MainActivity : AppCompatActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    val web = WebView(this)
    web.settings.javaScriptEnabled = true
    web.loadUrl("http://127.0.0.1:8080")
    setContentView(web)
  }
}
