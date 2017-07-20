
package com.sim.psensortest;

import android.app.Activity;
import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.PowerManager;
import android.util.Log;
import android.widget.TextView;

public class MainActivity extends Activity implements SensorEventListener {

    public static final String TAG = "SensorTest";

    // 调用距离传感器，控制屏幕
    private SensorManager mManager;// 传感器管理对象
    // 屏幕开关
    private PowerManager localPowerManager = null;// 电源管理对象
    private PowerManager.WakeLock localWakeLock = null;// 电源锁
    // TextView
    private TextView tv;// 基本上没啥用

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Log.d(TAG,"onCreate");

        tv = (TextView) findViewById(R.id.tv);

        mManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        // 获取系统服务POWER_SERVICE，返回一个PowerManager对象
        localPowerManager = (PowerManager) getSystemService(Context.POWER_SERVICE);
        // 获取PowerManager.WakeLock对象,后面的参数|表示同时传入两个值,最后的是LogCat里用的Tag
        localWakeLock = this.localPowerManager.newWakeLock(32, "MyPower");// 第一个参数为电源锁级别，第二个是日志tag
    }

    public void onResume() {
        super.onResume();
        mManager.registerListener(this, mManager.getDefaultSensor(Sensor.TYPE_PROXIMITY),// 距离感应器
                SensorManager.SENSOR_DELAY_NORMAL);// 注册传感器，第一个参数为距离监听器，第二个是传感器类型，第三个是延迟类型
    }

    public void onStop() {
        super.onStop();
        Log.d(TAG, "on stop");
    }

    public void onDestroy() {
        super.onDestroy();
        Log.d(TAG, "on destroy");
        if (mManager != null) {
            localWakeLock.release();// 释放电源锁，如果不释放finish这个acitivity后仍然会有自动锁屏的效果，不信可以试一试
            mManager.unregisterListener(this);// 注销传感器监听
        }
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        float[] its = event.values;
        Log.d(TAG,"its array:"+its+"sensor type :"+event.sensor.getType()+" proximity type:"+Sensor.TYPE_PROXIMITY);
        if (its != null && event.sensor.getType() == Sensor.TYPE_PROXIMITY) {
            System.out.println("its[0]:" + its[0]);
            tv.setText(its[0] + "");
            // 经过测试，当手贴近距离感应器的时候its[0]返回值为0.0，当手离开时返回1.0
            if (its[0] == 0.0) {// 贴近手机
                System.out.println("hands up");
                Log.d(TAG, "hands up in calling activity");
                if (localWakeLock.isHeld()) {
                    return;
                } else {
                    localWakeLock.acquire();// 申请设备电源锁
                }
            } else {// 远离手机
                System.out.println("hands moved");
                Log.d(TAG, "hands moved in calling activity");
                if (localWakeLock.isHeld()) {
                    return;
                } else {
                    localWakeLock.setReferenceCounted(false);
                    localWakeLock.release(); // 释放设备电源锁
                }
            }
        }

    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        // TODO 自动生成的方法存根

    }

}
