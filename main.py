import os
import sys
import time
import hashlib
import random
from faker import Faker
import json
from requests import post, get
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QColorDialog, QFontDialog
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.Qt import QUrl
from Ui_translate import Ui_MainWindow

class Translater(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(Translater, self).__init__(parent)
        self.setupUi(self)
        self.version = 2.7
        self.version_detail = '\n更新说明：\t增加字体、颜色设置；\n\t增加部分语音播报翻译结果；\n\t优化语音播放代码。'
        self.cwd = os.path.expanduser('~')
        self.con_out_voice.hide()
        self.label_H.show()
        self.data_dict = {
            'version': self.version,
            'input': '',
            'data_info': [],
            'language': '',
            'output': [],
            'in_color': '#000000',
            'in_font': ['Arial', 9, False, False, False],
            'out_color': '#000000',
            'out_font': ['Arial', 9, False, False, False]
        }
        self.set_info()

        f = Faker(locale='zh-CN')
        self.ua_all = f.user_agent()
        self.button_fy.clicked.connect(self.tran_act)
        self.button_clear.clicked.connect(self.clearact)
        self.actionverson.triggered.connect(self.versionact)
        self.actionhelp.triggered.connect(self.helpact)
        self.con_in_color.clicked.connect(lambda: self.change_coloract(1))
        self.con_in_size.clicked.connect(lambda: self.change_fontact(1))
        self.con_out_color.clicked.connect(lambda: self.change_coloract(0))
        self.con_out_size.clicked.connect(lambda: self.change_fontact(0))
        self.con_out_voice.clicked.connect(self.speak_act)

        self.player = QMediaPlayer()

    def set_info(self):
        if os.path.isfile(self.cwd + '/trandata.json'):
            with open(self.cwd + '/trandata.json', 'r', encoding='utf-8') as fp:
                self.data_dict = json.load(fp)
            if 'version' not in self.data_dict.keys():
                os.remove(self.cwd + '/trandata.json')
                self.data_dict['version'] = self.version
            else:
                if self.data_dict['version'] != self.version:
                    os.remove(self.cwd + '/trandata.json')
                    self.data_dict['version'] = self.version
                l = self.data_dict['language']
                self.set_language(l)
                in_font = self.data_dict['in_font']
                self.set_fontact(in_font, 1)
                out_font = self.data_dict['out_font']
                self.set_fontact(out_font, 0)
                in_color = self.data_dict['in_color']
                self.con_in.setStyleSheet('color:' + in_color)
                out_color = self.data_dict['out_color']
                self.con_out.setStyleSheet('color:' + out_color)

    def change_fontact(self, sxt):
        font_font, b = QFontDialog.getFont()
        if b:
            font_f = font_font.family()
            font_s = font_font.pointSize()
            font_b = font_font.bold()
            font_i = font_font.italic()
            font_u = font_font.underline()
            font_x = [font_f, font_s, font_b, font_i, font_u]
            if sxt == 1:
                self.con_in.setFont(font_font)
                self.data_dict['in_font'] = font_x
            else:
                self.con_out.setFont(font_font)
                self.data_dict['out_font'] = font_x

    def set_fontact(self, font, sxt):
        set_font = QFont()
        set_font.setFamily(font[0])
        set_font.setPointSize(font[1])
        set_font.setBold(font[2])
        set_font.setItalic(font[3])
        set_font.setUnderline(font[4])
        if sxt == 1:
            self.con_in.setFont(set_font)
        else:
            self.con_out.setFont(set_font)

    def change_coloract(self, sxt):
        color_color = QColorDialog.getColor()
        get_color = color_color.name()
        if sxt == 1:
            self.con_in.setStyleSheet('color:' + get_color)
            self.data_dict['in_color'] = get_color
        else:
            self.con_out.setStyleSheet('color:' + get_color)
            self.data_dict['out_color'] = get_color

    def get_info(self, context):
        ua = ''.join(self.ua_all.split('/')[1:])
        m = hashlib.md5()
        m.update(ua.encode('utf-8'))
        bv = m.hexdigest()
        ts = str(int(time.time() * 1000))
        salt = ts + str(random.randint(0,9))
        sign_str = 'fanyideskweb' + context + salt + 'Nw(nmmbP%A-r6U3EUn]Aj'
        mm = hashlib.md5()
        mm.update(sign_str.encode('utf-8'))
        sign = mm.hexdigest()
        self.data_dict['data_info'] = [bv, ts, salt, sign]
        return bv,ts,salt,sign

    def get_language(self):
        if self.radio_en.isChecked():
            language = 'en'
            self.con_out_voice.show()
            self.label_H.hide()
        if self.radio_ja.isChecked():
            language = 'ja'
            self.con_out_voice.show()
            self.label_H.hide()
        if self.radio_ko.isChecked():
            language = 'ko'
            self.con_out_voice.show()
            self.label_H.hide()
        if self.radio_ru.isChecked():
            language = 'ru'
            self.con_out_voice.hide()
            self.label_H.show()
        if self.radio_de.isChecked():
            language = 'de'
            self.con_out_voice.hide()
            self.label_H.show()
        if self.radio_fr.isChecked():
            language = 'fr'
            self.con_out_voice.show()
            self.label_H.hide()
        if self.radio_es.isChecked():
            language = 'es'
            self.con_out_voice.hide()
            self.label_H.show()
        if self.radio_pt.isChecked():
            language = 'pt'
            self.con_out_voice.hide()
            self.label_H.show()
        if self.radio_it.isChecked():
            language = 'it'
            self.con_out_voice.hide()
            self.label_H.show()
        if self.radio_ar.isChecked():
            language = 'ar'
            self.con_out_voice.hide()
            self.label_H.show()
        if self.radio_id.isChecked():
            language = 'id'
            self.con_out_voice.hide()
            self.label_H.show()
        if self.radio_vi.isChecked():
            language = 'vi'
            self.con_out_voice.hide()
            self.label_H.show()
        self.data_dict['language'] = language
        return language

    def set_language(self, l):
        if l == 'en':
            self.radio_en.setChecked(True)
        if l == 'ja':
            self.radio_ja.setChecked(True)
        if l == 'ko':
            self.radio_ko.setChecked(True)
        if l == 'ru':
            self.radio_ru.setChecked(True)
        if l == 'de':
            self.radio_de.setChecked(True)
        if l == 'fr':
            self.radio_fr.setChecked(True)
        if l == 'es':
            self.radio_es.setChecked(True)
        if l == 'pt':
            self.radio_pt.setChecked(True)
        if l == 'it':
            self.radio_it.setChecked(True)
        if l == 'ar':
            self.radio_ar.setChecked(True)
        if l == 'id':
            self.radio_id.setChecked(True)
        if l == 'vi':
            self.radio_vi.setChecked(True)

    def check_chinese(self, context):
        li = [
            '–', '—', '‘', '’', '“', '”', '…', '、', '。', '〈', '〉', '《',
            '》', '「', '」', '『', '』', '【','】', '〔', '〕', '！', '（', 
            '）','，', '．', '：', '；', '？',
            '!', '"', '#', '$', '%', '&',"'", '(', ')', '*', '+', ',', '-', 
            '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', 
            '`', '{', '|', '}', '~',
            '\n'
            ]
        for ch in context:
            if ch in li:
                pass
            elif ch < u'\u4E00' or ch > u'\u9FA5':
                return False
        return True

    def tran(self, context):
        bv, ts, salt, sign = self.get_info(context)
        l = self.get_language()
        headers = {
            'User-Agent': self.ua_all,
            'Referer': 'http://fanyi.youdao.com/',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=88532726@10.108.160.18; JSESSIONID=aaaCotdaKLvMH7QRFDoix; OUTFOX_SEARCH_USER_ID_NCOO=51303853.7527974; ___rl__test__cookies=' + ts
        }
        data = {
            'i':context,
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'ts': ts,
            'bv': bv,
            'doctype': 'json',
            'version':'2.1',
            'keyfrom':'fanyi.web',
            'action': 'lan-select',
        }
        if self.check_chinese(context):
            data['from'] = 'zh-CHS'
            data['to'] = l
        else:
            data['from'] = l
            data['to'] = 'zh-CHS'
            
        url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        response = post(url,data=data,headers=headers)
        data_dict = json.loads(response.text)
        data_dict_con = data_dict['translateResult']
        self.result = []
        for p in data_dict_con:
            for s in p:
                out_content = s['tgt']
                self.result.append(out_content)
        self.data_dict['output'] = self.result
        return self.result

    def get_speak(self):
        if self.radio_en.isChecked():
            speak = 'eng'
        elif self.radio_ja.isChecked():
            speak = 'jap'
        elif self.radio_ko.isChecked():
            speak = 'ko'
        elif self.radio_fr.isChecked():
            speak = 'fr'
        else:
            speak = 'eng'
            QMessageBox.warning(self, '错误', '不支持该语种发音，尝试采用英文发音。', QMessageBox.Ok)
            self.radio_en.setChecked(True)
        return speak

    def speak_act(self):
        content = self.con_out.toPlainText()
        url = 'http://tts.youdao.com/fanyivoice'
        le = self.get_speak()
        voice_url = url + '?word=' + content + '&le=' + le
        self.player.setMedia(QMediaContent(QUrl(voice_url)))
        self.player.setVolume(50)
        self.player.play()
        self.player.stateChanged.connect(self.play_state)
        self.con_out_voice.setDisabled(True)

    def play_state(self):
        self.con_out_voice.setEnabled(True)

    def tran_act(self):
        '''
        翻译
        '''
        context = self.con_in.toPlainText()
        if context != '':
            self.data_dict['input'] = context
            try:
                temp = self.tran(context)
                self.con_out.clear()
                for i in temp:
                    self.con_out.appendPlainText(i)
                    self.con_out.repaint()
            except:
                self.con_out.setPlainText('引擎错误！请检查网络链接！')
        else:
            self.con_out.setPlainText('请先输入原文！')

    def closeEvent(self, event):
        with open (self.cwd + '/trandata.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.data_dict, ensure_ascii=False, indent=4))

    def clearact(self):
        self.con_in.clear()
        self.con_out.clear()

    def versionact(self):
        '''
        版本菜单
        '''
        QMessageBox.about(self, '版本', '版本：V' + str(self.version) + self.version_detail)
    def helpact(self):
        '''
        帮助菜单
        '''
        QMessageBox.about(self, '帮助', '系统默认选择英文\n翻译后所选语种将被记录，作为下次翻译的默认语种。\n支持中文对多种语言、外文对中文的翻译\n系统自动判断用户输入语言是否为中文。\n非中文的原文，暂不支持自动判断语种。\n如需相应的外文翻译中文，请首先选择正确的外文语种。')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translate = Translater()
    translate.show()
    sys.exit(app.exec_())
