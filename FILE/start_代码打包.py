import os,sys
import shutil

lable_list = ['LOCAL_MODULE','LOCAL_COPY_HEADERS_TO','LOCAL_COPY_HEADERS','LOCAL_PACKAGE_NAME']
include_list = []
exe_list = []
shared_lib_list = []
static_lib_list = []
lib_list = []
vendorlib_list = []
module_list = []
apk_list = []
misc_list = []
jar_list = []

TARGET_OUT ="/home/liuyang/workplace/w80_apq8039/out/target/product/w80_8039/"
SIMOUT = "prebuilt_simcom/target/product/w80_8039/"

def search(mypath):
	if not mypath:
		print "path or cont is empty!"
		return
	_loopFolder(mypath)

def _loopFolder(mypath):
	arr = mypath.split('/')
	if not arr[-1].startswith('.'):
		if os.path.isdir(mypath):
			folderList = os.listdir(mypath)
			for x in folderList:
				_loopFolder(mypath+"/"+x)
		elif os.path.isfile(mypath):
			if os.path.basename(mypath) == "Android.mk":
				parse_makefile(mypath,lable_list[1]);
				parse_makefile(mypath,lable_list[0]);
				parse_makefile(mypath,lable_list[3]);

def look_same():
	hy_list = []
	sim_list = []
	f = open("HY11_Android.mk",'r')
	fcontent = f.readlines()
	f.close()
	for index,x in enumerate(fcontent):
		if "LOCAL_MODULE:" in str.replace(x,' ','').strip('\n'):
			hy_list.append(str.replace(x,' ','').strip('\n').split(":=")[-1])
	
	f = open("SIM_Android.mk",'r')
	fcontent = f.readlines()
	f.close()
	for index,x in enumerate(fcontent):
		if "LOCAL_MODULE:" in str.replace(x,' ','').strip('\n'):
			sim_list.append(str.replace(x,' ','').strip('\n').split(":=")[-1])
	for x in hy_list:
		for y in sim_list:
			if x == y:
				print y
	

def parse_makefile(filename,lable):
	f = open(filename,'r')
	fcontent = f.readlines()
	f.close()
	for index,x in enumerate(fcontent):
		if lable in x:
			parse_line(str.replace(x,' ','').strip('\n'))

def parse_line(line):
	if line.startswith('#'):
		return
	if line.startswith("LOCAL_COPY_HEADERS_TO"):
		include_list.append(line.split(":=")[-1])
	if line.startswith("LOCAL_PACKAGE_NAME:"):
		apk_list.append(line.split(":=")[-1])
	if line.startswith("LOCAL_MODULE:"):
		module_list.append(line.split(":=")[-1]);
		if(line.split(":=")[-1].startswith("lib")):
			lib_list.append(line.split(":=")[-1])
			vendorlib_list.append(line.split(":=")[-1])
		else:
			misc_list.append(line.split(":=")[-1])
			exe_list.append(line.split(":=")[-1])

def parse_misc(misc):
	for x in misc:
		if (len(x.split(".")) > 1):
			if (x.split(".")[-1] == "mbn"):
				continue
			if (x.split(".")[-1] == "conf"):
				continue
			if (x.split(".")[-1] == "acdb"):
				continue
			if (x.split(".")[-1] == "bin"):
				continue
			if (x.split(".")[-1] == "xml"):
				continue
			if (x.split(".")[-1] == "fw"):
				continue
			if (x.split(".")[-1] == "cfg"):
				continue
			if (x.split(".")[-1] == "idc"):
				continue
		else:
			#apk_list.append(x)
			exe_list.append(x)
			jar_list.append(x)
	#print apk_list
	

def apk_copy_from_out(apk):
	if not os.path.exists(SIMOUT+"system/app/"):
		os.makedirs(SIMOUT+"system/app/")
	for x in os.listdir(TARGET_OUT+"system/app/"):
		if x.split(".")[0] in apk:
			print(x.split(".")[0])
			shutil.copytree(TARGET_OUT+"system/app/"+x,SIMOUT+"system/app/"+x, 1)
	del apk_list[:]
	for apkf in os.listdir(SIMOUT+"system/app/"):
		apk_list.append(apkf.split('.')[0])
	return

def lib_copy_from_out(liblist):
	if not os.path.exists(SIMOUT+"system/lib/"):
		os.makedirs(SIMOUT+"system/lib/")
	for x in os.listdir(TARGET_OUT+"system/lib/"):
		if x.split(".")[0] in liblist:
			#print x
			shutil.copy(TARGET_OUT+"system/lib/"+x,SIMOUT+"system/lib/"+x)
	del lib_list[:]
	for libf in os.listdir(SIMOUT+"system/lib/"):
		lib_list.append(libf)
	return

def vendorlib_copy_from_out(liblist):
	if not os.path.exists(SIMOUT+"system/vendor/lib64/"):
		os.makedirs(SIMOUT+"system/vendor/lib64/")
	for x in os.listdir(TARGET_OUT+"system/vendor/lib64/"):
		if x.split(".")[0] in liblist:
		#if os.path.isfile(TARGET_OUT+"system/vendor/lib/"+x):
			shutil.copy(TARGET_OUT+"system/vendor/lib64/"+x,SIMOUT+"system/vendor/lib64/"+x)
	del vendorlib_list[:]
	for libf in os.listdir(SIMOUT+"system/vendor/lib64/"):
		vendorlib_list.append(libf)
	return

real_include_list = []
def include_copy_from_out(inc):
	temp = []
	real_temp = []
	for x in inc:
		temp.append(x.split('/')[0])
	for y in os.listdir(TARGET_OUT+"obj/include/"):
		if y in temp:
			#print y
			#copyFiles(TARGET_OUT+"obj/include/"+y,SIMOUT+"obj/include/"+y)
			if not os.path.exists(SIMOUT+"obj/include/"+y):
				shutil.copytree(TARGET_OUT+"obj/include/"+y,SIMOUT+"obj/include/"+y)
			real_temp.append(y)
	listfiles(SIMOUT+"obj/include/")
	zlist = []
	for z in file_list:
		zlist.append(z.split("/"))
	incstr = ''
	templist = []
	for z in zlist:
		z.pop(-1)
		incstr = "/".join(z)
		templist.append(incstr)
	del file_list[:]
	return list(set(templist))


def exe_copy_from_out(exelist):
	if not os.path.exists(SIMOUT+"system/bin/"):
		os.makedirs(SIMOUT+"system/bin/")
	for x in os.listdir(TARGET_OUT+"system/bin/"):
		if x in exelist:
			shutil.copy(TARGET_OUT+"system/bin/"+x,SIMOUT+"system/bin/"+x)
	del exe_list[:]
	for exef in os.listdir(SIMOUT+"system/bin/"):
		exe_list.append(exef)

def jar_copy_from_out(jarlist):
	if not os.path.exists(SIMOUT+"system/framework/"):
		os.makedirs(SIMOUT+"system/framework/")
	for x in os.listdir(TARGET_OUT+"system/framework/"):
		if x.split(".")[0] in jarlist:
			shutil.copy(TARGET_OUT+"system/framework/"+x,SIMOUT+"system/framework/"+x)
	del jar_list[:]
	for jarf in os.listdir(SIMOUT+"system/framework"):
		jar_list.append(jarf)

def copyFiles(sourceDir,targetDir):
	for file in os.listdir(sourceDir):
		sourceFile = os.path.join(sourceDir,  file) 
		targetFile = os.path.join(targetDir,  file)
		if os.path.isfile(sourceFile):
			if not os.path.exists(targetDir):
				os.makedirs(targetDir)
				if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
					open(targetFile, "wb").write(open(sourceFile, "rb").read())
		if os.path.isdir(sourceFile):
			First_Directory = False
			copyFiles(sourceFile, targetFile)

LOCAL_INCLUDE = SIMOUT + "obj/include/"
MK_INCLUDE_PATH = "../../.././target/product/w80_8039/obj/include/"
MK_APK_PATH = "../../.././target/product/w80_8039/system/app/"
MK_BIN_PATH = "../../.././target/product/w80_8039/system/bin/"
MK_LIB_PATH = "../../.././target/product/w80_8039/system/lib/"
MK_VENDORLIB_PATH = "../../.././target/product/w80_8039/system/vendor/lib64/"
def write_header_mk(rlist):
	makefile = open('myAndroid.mk','w')
	count = 0;
	makefile.write("PREBUILT_PATH := $(call my-dir)"+'\n')
	makefile.write("LOCAL_PATH := $(PREBUILT_PATH)"+'\n\n')
	for x in rlist:
		makefile.write("include $(CLEAR_VARS)"+"\n")
		makefile.write("LOCAL_COPY_HEADERS_TO := "+x+'\n')
		listfiles(SIMOUT+"obj/include/"+x)
		count = 0
		for ff in file_list:
			if count == 0:
				makefile.write("LOCAL_COPY_HEADERS := "+MK_INCLUDE_PATH+ff+'\n')
			else:
				makefile.write("LOCAL_COPY_HEADERS += "+MK_INCLUDE_PATH+ff+'\n')
			count = 1
		del file_list[:]
		makefile.write("include $(BUILD_COPY_HEADERS)"+"\n\n")
	makefile.close()

def write_apk_mk(apklist):
	makefile = open('myAndroid.mk','a')
	for x in apklist:
		makefile.write("include $(CLEAR_VARS)"+'\n')
		makefile.write("LOCAL_MODULE        := "+ x +'\n')
		makefile.write("LOCAL_MODULE_TAGS   := optional" +'\n')
		makefile.write("LOCAL_MODULE_CLASS  := APPS"+'\n')
		makefile.write("LOCAL_CERTIFICATE   := platform"+'\n')
		makefile.write("LOCAL_MODULE_SUFFIX := .apk"+'\n')
		makefile.write("LOCAL_SRC_FILES		:= "+MK_APK_PATH+x+".apk"+'\n')
		makefile.write("include $(BUILD_PREBUILT)"+'\n\n')
	makefile.close()
	f = open("option_deal.txt",'w')
	for x in apklist:
		f.write("PRODUCT_PACKAGES += "+x+"\n")
	f.close()
		

def write_bin_mk(exe_list):
	makefile = open('myAndroid.mk','a')
	for x in exe_list:
		makefile.write("include $(CLEAR_VARS)"+'\n')
		makefile.write("LOCAL_MODULE        := "+x+'\n')
		makefile.write("LOCAL_MODULE_TAGS   := optional"+'\n')
		makefile.write("LOCAL_MODULE_CLASS  := EXECUTABLES"+'\n')
		makefile.write("LOCAL_SRC_FILES     := "+MK_BIN_PATH+x+'\n')
		makefile.write("LOCAL_MODULE_PATH   := $(PRODUCT_OUT)/system/bin"+'\n')
		makefile.write("include $(BUILD_PREBUILT)"+'\n\n')
	makefile.close()

def write_jar_mk(jar_list):
	makefile = open('myAndroid.mk','a')
	makefile.write("PREBUILT_PATH := $(call my-dir)"+'\n')
	makefile.write("LOCAL_PATH := $(PREBUILT_PATH)"+'\n')
	for x in jar_list:
		makefile.write("include $(CLEAR_VARS)"+'\n')
		makefile.write("LOCAL_MODULE        := "+x+'\n')
		makefile.write("LOCAL_MODULE_TAGS   := optional"+'\n')
		makefile.write("LOCAL_MODULE_CLASS  := JAVA_LIBRARIES"+'\n')
		makefile.write("LOCAL_MODULE_SUFFIX := "+'\n')
		makefile.write("LOCAL_SRC_FILES 	:= "+x+'\n')
		makefile.write("include $(BUILD_PREBUILT)"+'\n\n')
	makefile.close()

def write_lib_mk(lib_list):
	makefile = open('myAndroid.mk','a')
	for x in lib_list:
		makefile.write("include $(CLEAR_VARS)"+'\n')
		makefile.write("LOCAL_MODULE        := "+x.split('.')[0]+'\n')
		makefile.write("LOCAL_MODULE_TAGS   := optional"+'\n')
		makefile.write("LOCAL_MODULE_CLASS  := SHARED_LIBRARIES"+'\n')
		makefile.write("LOCAL_MULTILIB      := 64"+'\n')
		makefile.write("LOCAL_MODULE_SUFFIX := .so" + '\n')
		makefile.write("LOCAL_SRC_FILES     := "+MK_LIB_PATH+x+'\n')
		makefile.write("LOCAL_MODULE_PATH   := $(PRODUCT_OUT)/system/lib64"+'\n')
		makefile.write("include $(BUILD_PREBUILT)"+'\n\n')
	makefile.close()

def write_vendorlib_mk(lib_list):
	makefile = open('myAndroid.mk','a')
	for x in lib_list:
		makefile.write("include $(CLEAR_VARS)"+'\n')
		makefile.write("LOCAL_MODULE        := "+x.split('.')[0]+'\n')
		makefile.write("LOCAL_MODULE_TAGS   := optional"+'\n')
		makefile.write("LOCAL_MODULE_CLASS  := SHARED_LIBRARIES"+'\n')
		makefile.write("LOCAL_MULTILIB      := 64"+'\n')
		makefile.write("LOCAL_MODULE_SUFFIX := .so" + '\n')
		makefile.write("LOCAL_MODULE_OWNER  := qcom" + '\n')
		makefile.write("LOCAL_SRC_FILES     := "+MK_VENDORLIB_PATH+x+'\n')
		makefile.write("LOCAL_MODULE_PATH   := $(PRODUCT_OUT)/system/vendor/lib64"+'\n')
		makefile.write("LOCAL_PROPRIETARY_MODULE := true" + '\n')
		makefile.write("include $(BUILD_PREBUILT)"+'\n\n')
	makefile.close()

file_list = []
def listfiles(srcDir):
	for file in os.listdir(srcDir):
		srcFile = os.path.join(srcDir,file)
		if os.path.isfile(srcFile):
			file_list.append(srcFile.replace(LOCAL_INCLUDE,''))
		if os.path.isdir(srcFile):
			listfiles(srcFile)


if __name__ == "__main__":
	search(sys.argv[1])

	real_include_list = include_copy_from_out(list(set(include_list)))
	write_header_mk(real_include_list)

	lib_copy_from_out(lib_list)
	write_lib_mk(lib_list)

	vendorlib_copy_from_out(vendorlib_list)
	write_vendorlib_mk(vendorlib_list)

	parse_misc(misc_list)

	apk_copy_from_out(apk_list)
	write_apk_mk(apk_list)

	exe_copy_from_out(exe_list)
	write_bin_mk(exe_list)

	jar_copy_from_out(jar_list)

	#look_same()
