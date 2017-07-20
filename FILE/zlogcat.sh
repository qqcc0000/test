while (true)
	do
		adb shell setprop service.adb.root 1
		adb wait-for-device
		date
		date1=`date +"%Y-%m-%d_%H:%M:%S"`
		echo $date1
		adb logcat -v time| tee $date1"_logcat.txt"
		sleep 1
	done
