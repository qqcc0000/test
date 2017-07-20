#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Android Robot 3.1
# This is a free software under GPL.
#
# Author: DiaoXuesong
# Bug report: wishcom@163.com
# ---------------------------------------------------------------------------
#
# Function:
# Screen cast via adb daemon, without java env.
# Usage:
#  arobot.py [-option]
# Example:
#  arobot.py
#  arobot.py -lcd
#  arobot.py -keypad

import subprocess,os
import threading
import socket,sys
import time

try:
    import Tkinter as tk
    import ttk
    from PIL import Image,ImageTk,ImageDraw
except:
    print 'Following module is needed:'
    print '- Tkinter: sudo apt-get install python-tk'
    print '- PIL: sudo apt-get install python-imaging-tk'
    sys.exit()

# Set DEBUG to True if you need know more running message
DEBUG = False

# Set USE_TTK to False if you need classic Tk/Tcl GUI-style
USE_TTK = True

'''
Key value definition refer from KeyEvent.java
public class KeyEvent extends InputEvent implements Parcelable {
    /** Key code constant: Unknown key code. */
    public static final int KEYCODE_UNKNOWN        = 0;
    public static final int KEYCODE_SOFT_LEFT      = 1;
    public static final int KEYCODE_SOFT_RIGHT      = 2;
    public static final int KEYCODE_HOME            = 3;
    public static final int KEYCODE_BACK            = 4;
    public static final int KEYCODE_CALL            = 5;
    public static final int KEYCODE_ENDCALL        = 6;
    public static final int KEYCODE_0              = 7;
    public static final int KEYCODE_1              = 8;
    public static final int KEYCODE_2              = 9;
    public static final int KEYCODE_3              = 10;
    public static final int KEYCODE_4              = 11;
    public static final int KEYCODE_5              = 12;
    public static final int KEYCODE_6              = 13;
    public static final int KEYCODE_7              = 14;
    public static final int KEYCODE_8              = 15;
    public static final int KEYCODE_9              = 16;
    public static final int KEYCODE_STAR            = 17;
    public static final int KEYCODE_POUND          = 18;
    public static final int KEYCODE_DPAD_UP        = 19;
    public static final int KEYCODE_DPAD_DOWN      = 20;
    public static final int KEYCODE_DPAD_LEFT      = 21;
    public static final int KEYCODE_DPAD_RIGHT      = 22;
    public static final int KEYCODE_DPAD_CENTER    = 23;
    public static final int KEYCODE_VOLUME_UP      = 24;
    public static final int KEYCODE_VOLUME_DOWN    = 25;
    public static final int KEYCODE_POWER          = 26;
    public static final int KEYCODE_CAMERA          = 27;
    public static final int KEYCODE_CLEAR          = 28;
    public static final int KEYCODE_A              = 29;
    public static final int KEYCODE_B              = 30;
    public static final int KEYCODE_C              = 31;
    public static final int KEYCODE_D              = 32;
    public static final int KEYCODE_E              = 33;
    public static final int KEYCODE_F              = 34;
    public static final int KEYCODE_G              = 35;
    public static final int KEYCODE_H              = 36;
    public static final int KEYCODE_I              = 37;
    public static final int KEYCODE_J              = 38;
    public static final int KEYCODE_K              = 39;
    public static final int KEYCODE_L              = 40;
    public static final int KEYCODE_M              = 41;
    public static final int KEYCODE_N              = 42;
    public static final int KEYCODE_O              = 43;
    public static final int KEYCODE_P              = 44;
    public static final int KEYCODE_Q              = 45;
    public static final int KEYCODE_R              = 46;
    public static final int KEYCODE_S              = 47;
    public static final int KEYCODE_T              = 48;
    public static final int KEYCODE_U              = 49;
    public static final int KEYCODE_V              = 50;
    public static final int KEYCODE_W              = 51;
    public static final int KEYCODE_X              = 52;
    public static final int KEYCODE_Y              = 53;
    public static final int KEYCODE_Z              = 54;
    public static final int KEYCODE_COMMA          = 55;
    public static final int KEYCODE_PERIOD          = 56;
    public static final int KEYCODE_ALT_LEFT        = 57;
    public static final int KEYCODE_ALT_RIGHT      = 58;
    public static final int KEYCODE_SHIFT_LEFT      = 59;
    public static final int KEYCODE_SHIFT_RIGHT    = 60;
    public static final int KEYCODE_TAB            = 61;
    public static final int KEYCODE_SPACE          = 62;
    public static final int KEYCODE_SYM            = 63;
    public static final int KEYCODE_EXPLORER        = 64;
    public static final int KEYCODE_ENVELOPE        = 65;
    public static final int KEYCODE_ENTER          = 66;
    public static final int KEYCODE_DEL            = 67;
    public static final int KEYCODE_GRAVE          = 68;
    public static final int KEYCODE_MINUS          = 69;
    public static final int KEYCODE_EQUALS          = 70;
    public static final int KEYCODE_LEFT_BRACKET    = 71;
    public static final int KEYCODE_RIGHT_BRACKET  = 72;
    public static final int KEYCODE_BACKSLASH      = 73;
    public static final int KEYCODE_SEMICOLON      = 74;
    public static final int KEYCODE_APOSTROPHE      = 75;
    public static final int KEYCODE_SLASH          = 76;
    public static final int KEYCODE_AT              = 77;
    public static final int KEYCODE_NUM            = 78;
    public static final int KEYCODE_HEADSETHOOK    = 79;
    public static final int KEYCODE_FOCUS          = 80;
    public static final int KEYCODE_PLUS            = 81;
    public static final int KEYCODE_MENU            = 82;
    public static final int KEYCODE_NOTIFICATION    = 83;
    public static final int KEYCODE_SEARCH          = 84;
    public static final int KEYCODE_MEDIA_PLAY_PAUSE= 85;
    public static final int KEYCODE_MEDIA_STOP      = 86;
    public static final int KEYCODE_MEDIA_NEXT      = 87;
    public static final int KEYCODE_MEDIA_PREVIOUS  = 88;
    public static final int KEYCODE_MEDIA_REWIND    = 89;
    public static final int KEYCODE_MEDIA_FAST_FORWARD = 90;
    public static final int KEYCODE_MUTE            = 91;
    public static final int KEYCODE_PAGE_UP        = 92;
    public static final int KEYCODE_PAGE_DOWN      = 93;
    public static final int KEYCODE_PICTSYMBOLS    = 94;
    public static final int KEYCODE_SWITCH_CHARSET  = 95;
    public static final int KEYCODE_BUTTON_A        = 96;
    public static final int KEYCODE_BUTTON_B        = 97;
    public static final int KEYCODE_BUTTON_C        = 98;
    public static final int KEYCODE_BUTTON_X        = 99;
    public static final int KEYCODE_BUTTON_Y        = 100;
    public static final int KEYCODE_BUTTON_Z        = 101;
    public static final int KEYCODE_BUTTON_L1      = 102;
    public static final int KEYCODE_BUTTON_R1      = 103;
    public static final int KEYCODE_BUTTON_L2      = 104;
    public static final int KEYCODE_BUTTON_R2      = 105;
    public static final int KEYCODE_BUTTON_THUMBL  = 106;
    public static final int KEYCODE_BUTTON_THUMBR  = 107;
    public static final int KEYCODE_BUTTON_START    = 108;
    public static final int KEYCODE_BUTTON_SELECT  = 109;
    public static final int KEYCODE_BUTTON_MODE    = 110;
    public static final int KEYCODE_ESCAPE          = 111;
    public static final int KEYCODE_FORWARD_DEL    = 112;
    public static final int KEYCODE_CTRL_LEFT      = 113;
    public static final int KEYCODE_CTRL_RIGHT      = 114;
    public static final int KEYCODE_CAPS_LOCK      = 115;
    public static final int KEYCODE_SCROLL_LOCK    = 116;
    public static final int KEYCODE_META_LEFT      = 117;
    public static final int KEYCODE_META_RIGHT      = 118;
    public static final int KEYCODE_FUNCTION        = 119;
    public static final int KEYCODE_SYSRQ          = 120;
    public static final int KEYCODE_BREAK          = 121;
    public static final int KEYCODE_MOVE_HOME      = 122;
    public static final int KEYCODE_MOVE_END        = 123;
    public static final int KEYCODE_INSERT          = 124;
    public static final int KEYCODE_FORWARD        = 125;
    public static final int KEYCODE_MEDIA_PLAY      = 126;
    public static final int KEYCODE_MEDIA_PAUSE    = 127;
    public static final int KEYCODE_MEDIA_CLOSE    = 128;
    public static final int KEYCODE_MEDIA_EJECT    = 129;
    public static final int KEYCODE_MEDIA_RECORD    = 130;
    public static final int KEYCODE_F1              = 131;
    public static final int KEYCODE_F2              = 132;
    public static final int KEYCODE_F3              = 133;
    public static final int KEYCODE_F4              = 134;
    public static final int KEYCODE_F5              = 135;
    public static final int KEYCODE_F6              = 136;
    public static final int KEYCODE_F7              = 137;
    public static final int KEYCODE_F8              = 138;
    public static final int KEYCODE_F9              = 139;
    public static final int KEYCODE_F10            = 140;
    public static final int KEYCODE_F11            = 141;
    public static final int KEYCODE_F12            = 142;
    public static final int KEYCODE_NUM_LOCK        = 143;
    public static final int KEYCODE_NUMPAD_0        = 144;
    public static final int KEYCODE_NUMPAD_1        = 145;
    public static final int KEYCODE_NUMPAD_2        = 146;
    public static final int KEYCODE_NUMPAD_3        = 147;
    public static final int KEYCODE_NUMPAD_4        = 148;
    public static final int KEYCODE_NUMPAD_5        = 149;
    public static final int KEYCODE_NUMPAD_6        = 150;
    public static final int KEYCODE_NUMPAD_7        = 151;
    public static final int KEYCODE_NUMPAD_8        = 152;
    public static final int KEYCODE_NUMPAD_9        = 153;
    public static final int KEYCODE_NUMPAD_DIVIDE  = 154;
    public static final int KEYCODE_NUMPAD_MULTIPLY = 155;
    public static final int KEYCODE_NUMPAD_SUBTRACT = 156;
    public static final int KEYCODE_NUMPAD_ADD      = 157;
    public static final int KEYCODE_NUMPAD_DOT      = 158;
    public static final int KEYCODE_NUMPAD_COMMA    = 159;
    public static final int KEYCODE_NUMPAD_ENTER    = 160;
    public static final int KEYCODE_NUMPAD_EQUALS  = 161;
    public static final int KEYCODE_NUMPAD_LEFT_PAREN = 162;
    public static final int KEYCODE_NUMPAD_RIGHT_PAREN = 163;
    public static final int KEYCODE_VOLUME_MUTE    = 164;
    public static final int KEYCODE_INFO            = 165;
    public static final int KEYCODE_CHANNEL_UP      = 166;
    public static final int KEYCODE_CHANNEL_DOWN    = 167;
    public static final int KEYCODE_ZOOM_IN        = 168;
    public static final int KEYCODE_ZOOM_OUT        = 169;
    public static final int KEYCODE_TV              = 170;
    public static final int KEYCODE_WINDOW          = 171;
    public static final int KEYCODE_GUIDE          = 172;
    public static final int KEYCODE_DVR            = 173;
    public static final int KEYCODE_BOOKMARK        = 174;
    public static final int KEYCODE_CAPTIONS        = 175;
    public static final int KEYCODE_SETTINGS        = 176;
    public static final int KEYCODE_TV_POWER        = 177;
    public static final int KEYCODE_TV_INPUT        = 178;
    public static final int KEYCODE_STB_POWER      = 179;
    public static final int KEYCODE_STB_INPUT      = 180;
    public static final int KEYCODE_AVR_POWER      = 181;
    public static final int KEYCODE_AVR_INPUT      = 182;
    public static final int KEYCODE_PROG_RED        = 183;
    public static final int KEYCODE_PROG_GREEN      = 184;
    public static final int KEYCODE_PROG_YELLOW    = 185;
    public static final int KEYCODE_PROG_BLUE      = 186;
    public static final int KEYCODE_APP_SWITCH      = 187;
    public static final int KEYCODE_BUTTON_1        = 188;
    public static final int KEYCODE_BUTTON_2        = 189;
    public static final int KEYCODE_BUTTON_3        = 190;
    public static final int KEYCODE_BUTTON_4        = 191;
    public static final int KEYCODE_BUTTON_5        = 192;
    public static final int KEYCODE_BUTTON_6        = 193;
    public static final int KEYCODE_BUTTON_7        = 194;
    public static final int KEYCODE_BUTTON_8        = 195;
    public static final int KEYCODE_BUTTON_9        = 196;
    public static final int KEYCODE_BUTTON_10      = 197;
    public static final int KEYCODE_BUTTON_11      = 198;
    public static final int KEYCODE_BUTTON_12      = 199;
    public static final int KEYCODE_BUTTON_13      = 200;
    public static final int KEYCODE_BUTTON_14      = 201;
    public static final int KEYCODE_BUTTON_15      = 202;
    public static final int KEYCODE_BUTTON_16      = 203;
    public static final int KEYCODE_LANGUAGE_SWITCH = 204;
    public static final int KEYCODE_MANNER_MODE    = 205;
    public static final int KEYCODE_3D_MODE        = 206;
    public static final int KEYCODE_CONTACTS        = 207;
    public static final int KEYCODE_CALENDAR        = 208;
    public static final int KEYCODE_MUSIC          = 209;
    public static final int KEYCODE_CALCULATOR      = 210;
    public static final int KEYCODE_ZENKAKU_HANKAKU = 211;
    public static final int KEYCODE_EISU            = 212;
    public static final int KEYCODE_MUHENKAN        = 213;
    public static final int KEYCODE_HENKAN          = 214;
    public static final int KEYCODE_KATAKANA_HIRAGANA = 215;
    public static final int KEYCODE_YEN            = 216;
    public static final int KEYCODE_RO              = 217;
    public static final int KEYCODE_KANA            = 218;
    public static final int KEYCODE_ASSIST          = 219;
    private static final int LAST_KEYCODE          = KEYCODE_ASSIST;

    private static final int KEYCODE_TEST_BASE    = 220;
    public static final int KEYCODE_POWER_TEST    = KEYCODE_TEST_BASE + 1;
    public static final int KEYCODE_HOME_TEST    = KEYCODE_TEST_BASE + 2;
    public static final int KEYCODE_BACK_TEST    = KEYCODE_TEST_BASE + 3;
    public static final int KEYCODE_MENU_TEST    = KEYCODE_TEST_BASE + 4;
    public static final int KEYCODE_SEARCH_TEST    = KEYCODE_TEST_BASE + 5;
    public static final int KEYCODE_CALL_TEST    = KEYCODE_TEST_BASE + 6;
    public static final int KEYCODE_ENDCALL_TEST     = KEYCODE_TEST_BASE + 7;
    public static final int KEYCODE_VOLUME_UP_TEST    = KEYCODE_TEST_BASE + 8;
    public static final int KEYCODE_VOLUME_DOWN_TEST      = KEYCODE_TEST_BASE + 9;
    public static final int KEYCODE_CAMERA_TEST    = KEYCODE_TEST_BASE + 10;
    public static final int KEYCODE_SPACE_TEST    = KEYCODE_TEST_BASE + 11;
    public static final int KEYCODE_FUNCTION_TEST    = KEYCODE_TEST_BASE + 12;
'''

# keynames is the key name list
# 'none': no keys in this grid
keynames = ['home', 'menu',  'back',  'srch',
            'call',    '^',    'end',  'none',
              '<',  'ok',      '>',  'vol+',
            'none',    'v',  'none',  'vol-',
              '1',    '2',      '3',  'none',
              '4',    '5',      '6',  'cam',
              '7',    '8',      '9', 'enter',
              '*',    '0',      '#'
            ]

# keyvalues is the key value list map with the keynames
# 0: no keys here
keyvalues = [ 3, 82, 4, 84,
              5, 19, 6,  0,
              21,23,22, 24,
              0, 20, 0, 25,
              8,  9,10, 0,
              11,12,13, 27,
              14,15,16, 66,
              17, 7,18
            ]

# Print Hex Buffer
def hexdump(buf = None):
    if buf != None:
        pstr = ''
        cnt = 0
        for x in buf:
            if (cnt + 1) % 8 == 0:
                pstr = '%s%02X\n' % (pstr, x)
            else:
                pstr = '%s%02X ' % (pstr, x)
            cnt = cnt + 1
        print pstr

# Read adb response, if 'OKAY' turn true
def readAdbResponse(s):
    if s != None:
        resp = s.recv(4)
        if DEBUG:
            print 'resp: %s' % repr(resp)

    if len(resp) != 4:
        print 'protocol fault (no status)'
        return False
   
    if resp == 'OKAY':
        return True
    elif resp == 'FAIL':
        resp = s.recv(4)
        if len(resp) < 4:
            print 'protocol fault (status len)'
            return False
        else:
            length = int(resp, 16)
            resp = s.recv(length)
            if len(resp) != length:
                print 'protocol fault (status read)'
                return False
            else:
                print resp
                return False
    else:
        print "protocol fault (status %02x %02x %02x %02x?!)", (resp[0], resp[1], resp[2], resp[3])
        return False

    return False

# Send adb shell command
def adbshellcommand(cmd):
    reply = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # waiting adb server start
    while True:
        try:
            s.connect(('127.0.0.1', 5037))
        except:
            os.system('adb start-server')
            time.sleep(2)
            continue
        else:
            break

    req_msg = 'host:transport-any'
    s.sendall('%04x' % len(req_msg))
    s.sendall(req_msg)
    if not readAdbResponse(s):
        return None

    req_msg = 'shell:%s' % cmd
    if DEBUG:
        print '%s' % req_msg
    s.sendall('%04x' % len(req_msg))
    s.sendall(req_msg)
    if readAdbResponse(s):
        reply = s.recv(4096)
        if DEBUG:
            hexdump(bytearray(reply))
    s.close()
   
    return reply

# Convert buffer to Int
def getInt(tbuf = None):
    if (tbuf != None):
        if DEBUG:
            hexdump(bytearray(tbuf))
        if len(tbuf) < 4:
            print 'buff len < 4'
            return 0
        else:
            if DEBUG:
                print 'parse: %02x %02x %02x %02x' % (tbuf[0],tbuf[1],tbuf[2],tbuf[3])
            intnum = tbuf[0]
            intnum = intnum + tbuf[1]*0x100
            intnum = intnum + tbuf[2]*0x10000
            intnum = intnum + tbuf[3]*0x1000000
            if DEBUG:
                print 'INT: %08x' % intnum
            return intnum
    else:
        return 0

# Parse fb header from buffer
def readHeader(tfb, ver, buf):
    if DEBUG:
        print 'readHeader: ver = %d' % ver
    if ver == 16:
        tfb.fb_bpp = 16
        tfb.fb_size = getInt(buf[0:4])
        tfb.fb_width = getInt(buf[4:8])
        tfb.fb_height = getInt(buf[8:12])
        tfb.red_offset = 11
        tfb.red_length = 5
        tfb.blue_offset = 5
        tfb.blue_length = 6
        tfb.green_offset = 0
        tfb.green_length = 5
        tfb.alpha_offset = 0
        tfb.alpha_length = 0
    elif ver == 1:
        tfb.fb_bpp = getInt(bytearray(buf[0:4]))
        tfb.fb_size = getInt(bytearray(buf[4:8]))
        tfb.fb_width = getInt(bytearray(buf[8:12]))
        tfb.fb_height = getInt(bytearray(buf[12:16]))
        tfb.red_offset = getInt(bytearray(buf[16:20]))
        tfb.red_length = getInt(bytearray(buf[20:24]))
        tfb.blue_offset = getInt(bytearray(buf[24:28]))
        tfb.blue_length = getInt(bytearray(buf[28:32]))
        tfb.green_offset = getInt(bytearray(buf[32:36]))
        tfb.green_length = getInt(bytearray(buf[36:40]))
        tfb.alpha_offset = getInt(bytearray(buf[40:44]))
        tfb.alpha_length = getInt(bytearray(buf[44:48]))
    else:
        return False
    return True

# Find the Touch input device and event
def get_touch_event():
    tp_names = ['ft5x06', 'gt818']
    output = adbshellcommand('getevent -S')
    if output == None:
        return None

    if DEBUG:
        print output
    dev = ''
    name = ''
    for line in output.splitlines():
        if '/dev/input/event' in line:
            line = line.split(':')
            if len(line) == 2:
                line = line[1]
                line = line.strip(' ')
                line = line.strip('"')
                dev = line
        elif 'name:' in line:
            line = line.split(':')
            if len(line) == 2:
                line = line[1]
                line = line.strip(' ')
                line = line.strip('"')
                name = line

        if (dev != '') and (name in tp_names):
            break

    if DEBUG:
        print '%s : %s' % (name, dev)

    if name in tp_names:
        return (name, dev)
    else:
        return None

# Do the touch action
def send_touch_event(action, x0, y0, x1 = None, y1 = None):
    # Note: input support tap & swipe after 4.1
    # so we need emulate TP via sendevent if tap or swipe fail
    if action == 'tap':
        resp = adbshellcommand('input tap %d %d' % (x0, y0))
        if 'Error' in resp:
            print 'Not support tap command'

            # get tp device
            tp = get_touch_event()

            if tp == None:
                return

            # down
            cmd_str = ''
            cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 3, 53, x0)
            cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 3, 54, y0)
            cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 3, 57, 0)
            cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 3, 48, 0)
            cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 0, 2, 0)
            cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 1, 330, 1)
            cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 0, 0, 0)

            # up
            cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 1, 330, 0)
            cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 0, 2, 0)
            cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 0, 0, 0)

            if DEBUG:
                print cmd_str
            adbshellcommand(cmd_str)
    elif action == 'swipe':
        resp = adbshellcommand('input swipe %d %d %d %d' % (x0, y0, x1, y1))
        if 'Error' in resp:
            print 'Not support tap command'
           
            # get tp device
            tp = get_touch_event()

            if tp == None:
                return

            step = 3
            stepx = abs(x1 - x0) / step
            stepy = abs(y1 - y0) / step
            x = x0
            y = y0

            for i in range(0, step + 1):
                if x0 < x1:
                    x = x0 + i * stepx
                else:
                    x = x0 - i * stepx

                if y0 < y1:
                    y = y0 + i * stepy
                else:
                    y = y0 - i * stepy

                cmd_str = ''
                cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 3, 53, x)
                cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 3, 54, y)
                cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 3, 57, 0)
                cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 3, 48, 0)
                cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 0, 2, 0)
                cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 1, 330, 1)
                cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 0, 0, 0)
                adbshellcommand(cmd_str)

            # up
            cmd_str = ''
            cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 1, 330, 0)
            cmd_str = cmd_str + 'sendevent %s %d %d %d;' % (tp[1], 0, 2, 0)
            cmd_str = cmd_str + 'sendevent %s %d %d %d' % (tp[1], 0, 0, 0)
            if DEBUG:
                print cmd_str
            adbshellcommand(cmd_str)

# Framebuffer Class
# Only record framebuffer attributs
class fb:
    fb_bpp = 0
    fb_size = 0
    fb_width = 0
    fb_height = 0
    red_offset = 0
    red_length = 0
    blue_offset = 0
    blue_length = 0
    green_offset = 0
    green_length = 0
    alpha_offset = 0
    alpha_length = 0
    fb_data = None

    def __init__(self):
        fb_bpp = 0
        fb_size = 0
        fb_width = 0
        fb_height = 0
        red_offset = 0
        red_length = 0
        blue_offset = 0
        blue_length = 0
        green_offset = 0
        green_length = 0
        alpha_offset = 0
        alpha_length = 0
        fb_data = None

# send key thread
class send_key_thread(threading.Thread):
    __tkapp = None
    __root = None
    __key = None
   
    def __init__(self, key):
        if DEBUG:
            print 'send_key_thread init'
        threading.Thread.__init__(self)
        self.thread_stop = False
        self.__key = key

    def devexist(self):
        p = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE)
        p.wait()
        devList = p.communicate()
        devList = devList[0].splitlines()
        if 'device' in devList[1]:
            if DEBUG:
                print devList[1]
            return True
        else:
            if DEBUG:
                print 'No adb device found'
            return False

    def sendKey(self):
        if DEBUG:
            print 'send_key: %s' % self.__key
        if self.__key in keynames:
            if self.devexist():
                if self.__key != 'none':
                    adbshellcommand('input keyevent %s' % str(keyvalues[keynames.index(self.__key)]))

    def run(self):
        if DEBUG:
            print 'send_key_thread run'
        self.sendKey()

    def stop(self):
        if DEBUG:
            print 'stop send_key_thread'
        self.thread_stop = True

# Kaypad Tkinter-Based GUI application
class KeypadApplication(tk.Frame):
    def __init__(self, master=None):
        if master == None:
            master = tk.Tk()
        tk.Frame.__init__(self, master, class_='KeypadApplication')
        self.createkeypad()
        self.grid()

    def createkeypad(self):
        # creat buttons from keymap with 4 buttons each row
        for btn_name in keynames:
            row_id = keynames.index(btn_name) / 4
            col_id = keynames.index(btn_name) % 4

            if btn_name != 'none':
                self.tbutton = tk.Button(self, name = btn_name, text=btn_name)
                self.tbutton['activebackground'] = '#BBBBBB'
                #self.tbutton['highlightcolor'] = '#BBBB00'
            else:
                self.tbutton = tk.Button(self, name = btn_name, text='')

            self.tbutton['width'] = 10
            if btn_name != 'none':
                self.tbutton.bind('<ButtonRelease-1>', self.sendKey)
                self.tbutton.grid(padx = 5, pady = 1, column = col_id, row = row_id)

    def devexist(self):
        p = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE)
        p.wait()
        devList = p.communicate()
        devList = devList[0].splitlines()
        if 'device' in devList[1]:
            if DEBUG:
                print devList[1]
            return True
        else:
            if DEBUG:
                print 'No adb device found'
            return False

    def sendKey(self, event=None):
        if DEBUG:
            print event.widget.winfo_name()
        keyname = event.widget.winfo_name()
        if keyname in keynames:
            sender = send_key_thread(keyname)
            sender.start()

# Kaypad Tkinter-Based GUI application
class ttkKeypadApplication(ttk.Frame):
    def __init__(self, master=None):
        if master == None:
            master = ttk.Tk()
        ttk.Frame.__init__(self, master, class_='ttkKeypadApplication')
        self.createkeypad()
        self.grid()

    def createkeypad(self):
        # creat buttons from keymap with 4 buttons each row
        for btn_name in keynames:
            row_id = keynames.index(btn_name) / 4
            col_id = keynames.index(btn_name) % 4

            if btn_name != 'none':
                self.tbutton = ttk.Button(self, name = btn_name, text=btn_name)
            else:
                self.tbutton = ttk.Button(self, name = btn_name, text='')

            self.tbutton['width'] = 10
            if btn_name != 'none':
                self.tbutton.bind('<ButtonRelease-1>', self.sendKey)
                self.tbutton.grid(padx = 5, pady = 1, column = col_id, row = row_id)

    def devexist(self):
        p = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE)
        p.wait()
        devList = p.communicate()
        devList = devList[0].splitlines()
        if 'device' in devList[1]:
            if DEBUG:
                print devList[1]
            return True
        else:
            if DEBUG:
                print 'No adb device found'
            return False

    def sendKey(self, event=None):
        if DEBUG:
            print event.widget.winfo_name()
        keyname = event.widget.winfo_name()
        if keyname in keynames:
            sender = send_key_thread(keyname)
            sender.start()

# LCD Tkinter-Based GUI application
class LcdApplication(tk.Frame):
    __img_factor = 1.00 # image resize rate
    __lcd = None # the label widget
    __keepupdate = True
    __im = None
    __rotate = 0

    # record mouse start & end point location
    __start = [0, 0]
    __end = [0, 0]

    def __init__(self, master=None):
        if DEBUG:
            print 'LcdApplication: __init__'
        if master == None:
            master = tk.Tk()
        tk.Frame.__init__(self, master, class_='LcdApplication')
        self.__rotate = 0
        self.createlcd()
        self.grid()

    def createlcd(self):
        # creat label as lcd
        if DEBUG:
            print 'LcdApplication: createlcd'

        # make default image display on label
        image = Image.new(mode = 'RGB', size = (240, 320), color = '#000000')
        draw = ImageDraw.Draw(image)
        draw.text((80, 100), 'Connecting...')
        self.__im = ImageTk.PhotoImage(image)

        # create label with image option
        self.__lcd = tk.Label(self, image=self.__im)
        self.__lcd.bind('<Button-1>', self.click_label)
        self.__lcd.bind('<ButtonRelease-1>', self.click_label)
        self.__lcd.bind('<ButtonRelease-3>', self.rightclick_label)

        # disply label on frame
        self.__lcd.grid()

    # To serve right click on label widget
    def rightclick_label(self, event=None):
        if DEBUG:
            print 'Type: %s' % event.type
        self.__rotate = (self.__rotate + 90) % 360
        print "rotate: %d" % self.__rotate

    # To serve left click on label widget
    def click_label(self, event=None):
        if DEBUG:
            print 'Type: %s' % event.type
        if event.type == '4':
            # record mouse left button down
            if DEBUG:
                print 'Click at: (%d, %d)' % (event.x, event.y)
            self.__start[0] = int(float(event.x) / float(self.__img_factor))
            self.__start[1] = int(float(event.y) / float(self.__img_factor))
            self.__end = None
        elif event.type == '5':
            # record mouse left button up
            if DEBUG:
                print 'Release at: (%d, %d)' % (event.x, event.y)
            self.__end = [0, 0]
            self.__end[0] = int(float(event.x) / float(self.__img_factor))
            self.__end[1] = int(float(event.y) / float(self.__img_factor))

        # Do not report touch event during mouse down
        if self.__end == None:
            return
       
        if abs(self.__start[0] - self.__end[0]) < 2 and \
          abs(self.__start[1] - self.__end[1]) < 2 :
            # mouse action: tap
            send_touch_event('tap', self.__start[0], self.__start[1])
        else:
            # mouse action: swipe
            send_touch_event('swipe', self.__start[0], self.__start[1], self.__end[0], self.__end[1])

    def stop(self):
        if DEBUG:
            print 'LcdApplication: stop'
        self.__keepupdate = False

    # screen capture via socket from adb server
    def updatelcd_sock(self):
        if DEBUG:
            print 'LcdApplication: updatelcd_sock'
        # Max display area size on label widget
        #max_lcd_w = 1024
        #max_lcd_h = 600
        max_lcd_w = 1440
        max_lcd_h = 720


        dev_sn = ''
        hdrsize = 0
        myfb = fb()
        refresh_count = 0 # record refresh count

        while self.__keepupdate:
            # Get device SerialNumber from ADB server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect(('127.0.0.1', 5037))
            except:
                os.system('adb start-server')
                time.sleep(2)
                continue

            req_msg = 'host:devices'
            s.sendall('%04x' % len(req_msg))
            s.sendall(req_msg)
            if readAdbResponse(s):
                len_str = s.recv(4)
                if len(len_str) < 4:
                    continue
                length = int(len_str, 16)
                dev_info = s.recv(length)
                if '\t' in dev_info:
                    dev_sn = dev_info[0:dev_info.index('\t')]
                else:
                    dev_sn = ''
                if DEBUG:
                    print 'dev serial: %s' % dev_sn
            s.recv(1024) # receive all rest data
            s.close()

            if dev_sn == '':
                continue

            # Get framebuffer from ADB server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', 5037))
            req_msg = 'host:transport:%s' % dev_sn
            s.sendall('%04x' % len(req_msg))
            s.sendall(req_msg)
            if not readAdbResponse(s):
                s.close()
            else:
                if DEBUG:
                    print 'ready to transport'
                req_msg = 'framebuffer:'
                s.sendall('%04x' % len(req_msg))
                s.sendall(req_msg)
                if not readAdbResponse(s):
                    s.close()
                else:
                    reply = s.recv(4)
                    if len(reply) < 4:
                        continue
                   
                    fbver = ord(reply[0]) + \
                            ord(reply[1]) * 0x100 + \
                            ord(reply[2]) * 0x10000 + \
                            ord(reply[3]) * 0x1000000
                    if DEBUG:
                        print 'fbver: %08x' % fbver

                    # Get fb header size
                    if fbver == 16:
                        hdrsize = 3
                    elif fbver == 1:
                        hdrsize = 12
                    else:
                        hdrsize = 0;
                    if DEBUG:
                        print 'fb header size: %d' % hdrsize

                    # read the header
                    header = s.recv(hdrsize * 4)
                    if len(header) < (hdrsize * 4):
                        continue

                    if DEBUG:
                        hexdump(bytearray(header))
                    readHeader(myfb, fbver, header)
                    if DEBUG:
                        print 'bpp: %d' % myfb.fb_bpp
                        print 'size: %d' % myfb.fb_size
                        print 'width: %d' % myfb.fb_width
                        print 'height: %d' % myfb.fb_height
                        print 'red_offset: %d' % myfb.red_offset
                        print 'red_length: %d' % myfb.red_length
                        print 'blue_offset: %d' % myfb.blue_offset
                        print 'blue_length: %d' % myfb.blue_length
                        print 'green_offset: %d' % myfb.green_offset
                        print 'green_length: %d' % myfb.green_length
                        print 'alpha_offset: %d' % myfb.alpha_offset
                        print 'alpha_length: %d' % myfb.alpha_length

                    # read fb buffer
                    rcvcnt = 0
                    readbyte = 0
                    imagebuff = []
                    while True:
                        if (rcvcnt < myfb.fb_size):
                            readbyte = myfb.fb_size - rcvcnt
                        else:
                            break
                        resp = s.recv(readbyte)
                        if DEBUG:
                            print 'read byte: %d' % len(resp)
                        rcvcnt = rcvcnt + len(resp);
                        imagebuff.extend(resp)
                        if len(resp) == 0:
                            break

                    if DEBUG:
                        print 'total rcv byte: %d' % rcvcnt
                    reply = s.recv(10)
                    s.close()
                    myfb.fb_data = bytearray(imagebuff)

                    if len(imagebuff) < myfb.fb_size:
                        continue

                    # convert raw-rgb to image
                    image = Image.frombuffer('RGBA',
                                            (myfb.fb_width, myfb.fb_height),
                                            myfb.fb_data,
                                            'raw',
                                            'RGBA',
                                            0,
                                            1)

                    lcd_w = image.size[0]
                    lcd_h = image.size[1]
                    if DEBUG:
                        print 'LCD size: %d x %d' % (lcd_w,lcd_h)
                    factor_w = 1.00
                    factor_h = 1.00
                    if lcd_w > max_lcd_w:
                        img_w = max_lcd_w
                        factor_w = float(img_w)/float(lcd_w)
                    if lcd_h > max_lcd_h:
                        img_h = max_lcd_h
                        factor_h = float(img_h)/float(lcd_h)
                    factor = min([factor_w, factor_h])
                    self.__img_factor = factor

                    # Keep the rate of w:h
                    img_w = int(lcd_w * factor)
                    img_h = int(lcd_h * factor)
                    if DEBUG:
                        print 'Image size: %d x %d' % (img_w, img_h)

                    # resize image
                    if (factor < 1.00):
                        image = image.resize((img_w, img_h))

                    # rotate image
                    if self.__rotate != 0:
                        image = image.rotate(self.__rotate)

                    if self.__lcd != None:
                        try:
                            # save image to local path
                            if DEBUG:
                                refresh_count = refresh_count + 1
                                image_name = 'image_%d.png' % refresh_count
                                image.save(image_name, format='PNG')
                            new_image = ImageTk.PhotoImage(image)
                            self.__im = new_image
                            self.__lcd['image'] = self.__im
                        except:
                            continue

# keypad window thread
class arobot_keys(threading.Thread):
    __tkapp = None
    __root = None
   
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = False

    def run(self):
        if DEBUG:
            print 'run arobot_keys'
        self.__root = tk.Tk()
        if USE_TTK:
            self.__tkapp = ttkKeypadApplication(master=self.__root)
        else:
            self.__tkapp = KeypadApplication(master=self.__root)
        self.__tkapp.master.title('ARobot3.0-Keypad')
        self.__tkapp.grid()
        self.__tkapp.mainloop()
        if DEBUG:
            print 'exit arobot_keys mainloop'

    def stop(self):
        if DEBUG:
            print 'stop arobot_keys'
        if self.__tkapp != None:
            self.__tkapp.quit()
        self.thread_stop = True

# screen windows thread
class arobot_lcd(threading.Thread):
    __tkapp = None
    __root = None
   
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = False

    def run(self):
        if DEBUG:
            print 'run arobot_lcd'
        self.__root = tk.Tk()
        self.__tkapp = LcdApplication(master=self.__root)
        self.__tkapp.master.title('ARobot3.0-Lcd')
        t = threading.Timer(1, self.__tkapp.updatelcd_sock)
        t.start()
        self.__tkapp.grid()
        self.__tkapp.mainloop()
        if DEBUG:
            print 'exit arobot_lcd mainloop'
        self.__tkapp.stop()

    def stop(self):
        if DEBUG:
            print 'stop arobot_lcd'
        self.thread_stop = True
        if self.__tkapp != None:
            self.__tkapp.stop()
            self.__tkapp.quit()

def arobot_main(prog):
    if prog == None:
        return

    if prog == 'lcd':
        lcd_thread = arobot_lcd()
        lcd_thread.start()

    if prog == 'keypad':
        keypad_thread = arobot_keys()
        keypad_thread.start()

def usage():
    print '--------------------------------------------'
    print 'Arobot 3.1'
    print 'This is a tool to control Android device via ADB'
    print 'usage: python %s [option]' % sys.argv[0]
    print 'option:'
    print '  -keypad    run keypad'
    print '  -lcd        run lcd'
    print '--------------------------------------------'

if __name__ == '__main__':
    prog_name = sys.argv[0]
    if '--debug' in  sys.argv:
        DEBUG = True

    if DEBUG:
        if len(sys.argv) == 2:
            cmd_str = 'python %s -keypad --debug' % prog_name
            p1 = subprocess.Popen(cmd_str, shell=True)
            cmd_str = 'python %s -lcd --debug' % prog_name
            p2 = subprocess.Popen(cmd_str, shell=True)
        elif len(sys.argv) == 3:
            if sys.argv[1] == '-keypad':
                arobot_main('keypad')
            elif sys.argv[1] == '-lcd':
                arobot_main('lcd')
            else:
                usage()
    else:
        if len(sys.argv) == 1:
            # Do not wast your time on threading, it is disaster working with tk!
            # I have tried many ways to open multi-windows via Tk and Threading
            # but fail! or linux ok but windows fail, so, just use the subprocess!
            cmd_str = 'python %s -keypad' % prog_name
            p1 = subprocess.Popen(cmd_str, shell=True)
            cmd_str = 'python %s -lcd' % prog_name
            p2 = subprocess.Popen(cmd_str, shell=True)
        elif len(sys.argv) == 2:
            if sys.argv[1] == '-keypad':
                arobot_main('keypad')
            elif sys.argv[1] == '-lcd':
                arobot_main('lcd')
            else:
                usage()       
        else:
            usage()
