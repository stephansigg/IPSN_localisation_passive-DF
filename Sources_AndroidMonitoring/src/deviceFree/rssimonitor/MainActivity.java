package deviceFree.rssimonitor;

import java.io.DataOutputStream;
import java.io.IOException;
import java.util.ArrayList;

import eu.chainfire.libsuperuser.Shell;
import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.view.View;

public class MainActivity extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}
		
	public void startSetup(View view){
		Thread th = new Thread(new Runnable() {
			
			@Override
			public void run() {
				ArrayList<String> liste = new ArrayList<String>();
				liste.add("cd /sdcard/");
				liste.add("sh ./setup.sh");
				liste.add("sleep 10");
				//liste.add("sh /sdcard/startTcpdump.sh &");
				liste.add("tcpdump -w /sdcard/myTestOutput140207.cap &");
				liste.add("sleep 20");
				liste.add("killall tcpdump");
				Shell.SU.run(liste);
			}
		});
		th.start();
	}
	
	
	public void startTcpdump(View view){
		// This is not actually necessary. 
		// Better: function to send the data via bluetooth somewhere
		Thread th2 = new Thread(new Runnable() {
			@Override
			public void run() {
				ArrayList<String> liste = new ArrayList<String>();
				liste.add("killall tcpdump");
				Shell.SU.run(liste);
			}
		});
		th2.start();
		
	}
	
}
	