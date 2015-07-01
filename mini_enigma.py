import sys
import string
from random import randrange
from time import sleep as zzz


class EnigmaDevice:
    def __init__(self):
        self.wheels = [{0: 13, 1: 25, 2: 5, 3: 9, 4: 14, 5: 6, 6: 21, 7: 11, 8: 8, 9: 24, 10: 22, 11: 15, 12: 3, 13: 10,
                        14: 20, 15: 16, 16: 18, 17: 12, 18: 7, 19: 1, 20: 19, 21: 4, 22: 2, 23: 23, 24: 17, 25: 0},

                       {0: 5, 1: 17, 2: 23, 3: 1, 4: 6, 5: 24, 6: 13, 7: 3, 8: 0, 9: 16, 10: 14, 11: 7, 12: 21, 13: 2,
                        14: 12, 15: 8, 16: 10, 17: 4, 18: 25, 19: 19, 20: 11, 21: 22, 22: 20, 23: 15, 24: 9, 25: 18},

                       {0: 0, 1: 12, 2: 18, 3: 22, 4: 1, 5: 19, 6: 8, 7: 24, 8: 21, 9: 11, 10: 9, 11: 2, 12: 16, 13: 23,
                        14: 7, 15: 3, 16: 5, 17: 25, 18: 20, 19: 14, 20: 6, 21: 17, 22: 15, 23: 10, 24: 4, 25: 13},

                       {0: 21, 1: 22, 2: 23, 3: 24, 4: 25, 5: 0, 6: 1, 7: 2, 8: 3, 9: 4, 10: 5, 11: 6, 12: 7, 13: 8,
                        14: 9, 15: 10, 16: 11, 17: 12, 18: 13, 19: 14, 20: 15, 21: 16, 22: 17, 23: 18, 24: 19, 25: 20}]

        txt = ["\n\n\n", "*-"*12+'\n'+" Mini_enigma\n\n by Nathan R Smith\n github.com/NSMobileCS\n narsmith012@gmail.com\n"+'-*'*12,
               '\n\n', "This script simulates one version of the historical Enigma",
               "encryption device that Alan Turing helped break during WWII.",
               "It encodes & decodes text using 4 virtual code-wheels.\n",
               "For historical accuracy, text displays in all caps.",
               '\nVerbose mode allows you to \'see it working\' by ',
               "printing program state every cycle",
              "(0)verbose mode off (1)normal verbose mode (2)ultra verbose mode"]

        self.verbose = 1

        for line in txt:
            print(line)
            zzz(1.1)
        seeitworking = input("Selection (press Enter for default): ")
        if seeitworking == '1':
            pass
        elif seeitworking == '2':
            self.verbose = 2
        else:
            self.verbose = 0

    def untranslate(self, n):
        """changes between single position number / 4 position vals """

        d = (n // 26 ** 3) % 26
        c = (n // 26 ** 2) % 26
        b = (n // 26) % 26
        a = n % 26
        if self.verbose > 1:
            print(a, b, c, d)
        return (a, b, c, d)


    def translate(self, stg):
        """changes between 4 position vals / single position number """
        n = 0
        for i in range(len(stg)):
            n += stg[i] * 26 ** i
        return n


    def make_wheel(self):
        """
        Makes a pseudo-random codewheel & returns it as a string.
        """
        asc = string.ascii_uppercase
        buildindexes = []
        while len(buildindexes) < 26:
            n = randrange(26)
            if n not in buildindexes:
                buildindexes.append(n)
            else:
                continue
        wheel = ""
        for i in buildindexes:
            wheel += asc[i]
        return wheel


    def mw(self):
        """makes a list of 4 pseudorandom codewheels, each in dict form """
        wls = []
        for i in range(4):
            d = dict()
            w = self.make_wheel()
            for k in range(len(w)):
                d[k] = string.ascii_uppercase.index(w[k])
            wls.append(d)
        self.wheels = wls
        print('code wheels changed')
        print('new code wheels:')
        print(self.wheels, '\n')



    def de(self, code, stg):
        """Decoder """
        code = code.upper()
        whl = self.rev_wls(self.wheels)
        asnum = []
        plain = []
        for i in range(len(code)):
            if code[i] in list(string.ascii_uppercase):
                x = list(string.ascii_uppercase).index(code[i])
                asnum.append(x)
            else:
                asnum.append(code[i])
        for i in asnum:
            if i in range(0, 26):
                for w in range(len(whl) - 1, -1, -1):
                    i = whl[w][i]
                    i -= stg[w]
                    i = i % 26
                    if self.verbose > 1:
                        print("w ", w, whl[w])
                        print(" - - - - ")
                        print("i ", i)
                plain.append(i)
                stg = self.translate(stg) + 1
                stg = self.untranslate(stg)
                if self.verbose:
                    print("Wheels\' position on last character decoded = ", stg)
            else:
                plain.append(i)
        if self.verbose:
            print(plain)
        for i in range(len(plain)):
            if plain[i] in range(26):
                plain[i] = string.ascii_uppercase[plain[i]]
        return ''.join(plain)



    def en(self, txt, stg):
        """ Encoder """
        txt = txt.upper()
        cod = []
        asnum = []
        for i in range(len(txt)):
            if txt[i] in list(string.ascii_uppercase):
                x = list(string.ascii_uppercase).index(txt[i])
                asnum.append(x)
            else:
                asnum.append(txt[i])
        if self.verbose > 1:
            print('as numbers where pos: ', asnum)
            print(" ... ")
        for i in asnum:
            if i in range(0, 26):
                if self.verbose:
                    print('setting at ', stg, 'i comes in as', i)
                for spin in range(len(self.wheels)):
                    i += stg[spin]
                    if self.verbose > 1:
                        print(i)
                    i = self.wheels[spin][i % 26]
                    if self.verbose > 1:
                        print(spin, self.wheels[spin], 'i = ', i)
                cod.append(string.ascii_uppercase[i])

                stg = self.translate(stg) + 1
                stg = self.untranslate(stg)
                if self.verbose:
                    print("Wheels\' position on last character encoded = ", stg)
            else:
                cod.append(i)
        return ''.join(cod)


    def reverse_whls(self, wheel):
        wa = [''] * 26
        wb = [''] * 26
        wc = [''] * 26
        wd = [''] * 26
        for k in wheel[0]:
            wa[wheel[0][k]] = k
            wb[wheel[1][k]] = k
            wc[wheel[2][k]] = k
            wd[wheel[3][k]] = k
        return [wa, wb, wc, wd]


    def rev_wls(self, wls):
        wl = self.reverse_whls(wls)
        dl = []
        for i in wl:
            wd = dict()
            for k in range(len(i)):
                wd[k] = i[k]
            dl.append(wd)
        return dl

    def uiEncode(self):
        stg = []
        man = input("Enter #### to generate pseudo-random codewheel position setting or presss any key to input manually: ")
        if man == "####":
            for i in range(4):
                stg.append(randrange(26))
            print(stg)
        else:
            try:
                for i in range(4):
                    ip = input("Enter pos setting #%s of 4: " % str(i + 1))
                    stg.append(int(ip))
            except ValueError:
                print('there was a typo (ValueError). please try again')
                return self.uiLoop()
        print("Setting is: %s " % str(stg))
        plain = input("Enter text to encode: ")
        code = self.en(plain, stg)
        print("Result: ", code)
        anykey = input("\'Q\' to quit; otherwise return to main menu. ")
        if anykey.lower() == 'q':
            return sys.exit(0)
        return self.uiLoop()

    def uiDecode(self):
        stg = []
        try:
            for i in range(4):
                ip = input("Enter pos setting #%s of 4: " % str(i + 1))
                stg.append(int(ip))
        except ValueError:
            print('there was a typo (ValueError). please try again')
            return self.uiLoop()
        code = input("Enter text to decode: ")
        plain = self.de(code, stg)
        print("Result: ", plain)
        anykey = input("\'Q\' to quit; otherwise return to main menu. ")
        if anykey.lower() == 'q':
            return sys.exit(0)
        return self.uiLoop()

    def uiMkWheel(self):
        w = input("(1) Print current codewheels to screen (2) Generate new pseudo-random codewheels (3) Enter new codewheels manually\n\n\tYour choice: ")
        try:
            if w == '1':
                print(self.wheels)
            elif w == '2':
                wls = self.mw()
            elif w == '3':
                wls = eval(input("Enter codewheels as a list of Python Dictionaries: "))
                if len(wls) == 4 and type(wls) == type([]):
                    self.wheels = wls
                else:
                    print("code wheel format not accepted; no changes made. please ensure correct format and try again")
            return self.uiLoop()
        except (ValueError, TypeError) as xception:
            print("Operation failed. Exception: %s" % xception)

    def uiLoop(self):
        print('\n'*2 + '|'*29, "\n|| Mini_enigma | Main Menu ||\n" + '|'*29, '\n')
        wls = self.wheels
        haswheel = " *ATTN: Missing codewheels. Please select this option (#3) to generate * "
        try:
            if len(wls) == 4:
                haswheel = "(Note: Default codewheels enabled. Change to add another layer of complexity)"
        except Exception:
            haswheel = " *ATTN: Missing codewheels. Please select this option (#3) to generate * "
        print("Options:")
        print("1 \tEncode Message")
        print("2 \tDecode Message")
        print("3 \tView/add/change codewheels %s " % haswheel)
        upick = input("\nSelect # or press 'Q' to quit: ")
        if upick.lower() == 'q':
            print("\n\nThanks for using my mini_enigma demo project.",
                  "\nI hope you found it interesting &/or educational.",
                  "\nNot for real cryptographic purposes - consider that",
                  "\nPolish, British, & other Allied cryptologists were",
                  "\nalready breaking these types of code in the 1930\'s-\'40\'s...\n")
            return sys.exit(0)
        try:
            upick = int(upick)
        except ValueError:
            return self.uiLoop()
        if upick == 1:
            self.uiEncode()
        elif upick == 2:
            self.uiDecode()
        elif upick == 3:
            self.uiMkWheel()
        return self.uiLoop()


if __name__ == '__main__':
    enigma = EnigmaDevice()
    enigma.uiLoop()
