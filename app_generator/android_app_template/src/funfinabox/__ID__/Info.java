package funfinabox.__ID__;

import funfinabox.__ID__.R;
import android.app.Activity;
import android.os.Bundle;

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
    }
}
