package funfinabox.__ID__;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.text.method.LinkMovementMethod;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

public class Info extends Activity
{
	public static final String TAG = "__ID__";
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        if (!LauncherReceiver.isLaunched()) {
        	LauncherReceiver.launch(this);
        }
        
        ((TextView)findViewById(R.id.contact_email)).setMovementMethod(LinkMovementMethod.getInstance());
        
        ((Button)findViewById(R.id.uninstall_button)).setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View v) {
				Uri packageURI = Uri.parse("package:" + getPackageName());
				Intent uninstallIntent = new Intent(Intent.ACTION_DELETE, packageURI);
				startActivity(uninstallIntent);
			}
		});
        
        ((ImageView)findViewById(R.id.logo_button)).setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View v) {
				String url = "http://www.funf.org/inabox/";  
				Intent i = new Intent(Intent.ACTION_VIEW);  
				i.setData(Uri.parse(url));  
				startActivity(i);  
			}
		});
    }
}
