class Checker():
    def checkLogin(self, email, password):
        message = ""
        codes = ["email", "password"]
        values = [email, password]
        for i in range(len(codes)):
            if(len(values[i]) == 0):
                return "Field " + codes[i] + " is missing."
        return  message

    def checkEmpty(self, jmbg, forename, surname, email, password):
        codes = ["jmbg", "forename", "surname", "email", "password"]
        values = [jmbg, forename, surname, email, password]
        message = ""
        for i in range(len(codes)):
            if(len(values[i]) == 0):
                message += "Field " + codes[i] + " is missing."
                return message
        return message
    def checkJmbg(self, jmbg):
        err = "Invalid jmbg."
        if(not jmbg.isnumeric()):
            return err
        digits = [int(c) for c in jmbg]
        value = int(jmbg[0:2])
        if(value > 31 or value < 1):
            return err
        value = int(jmbg[2:4])
        if(value > 12 or value < 1):
            return err
        value = int(jmbg[7:9])
        if(value < 70):
            return err

        digit = int(jmbg[12])
        tmp = 0
        cur = 0
        for i in range(6,len(digits) - 1):
            tmp = tmp + (7 - cur) * (digits[i - 6] + digits[i])
            cur = cur + 1
        tmp %= 11

        tmp = 11 - tmp

        if(tmp != digit):
            return err
        return ""

    def checkPassword(self, password):
        if(len(password) < 8):
            return "Invalid password."
        okSmall = False
        okBig = False
        okDigit = False;
        if(any(c.islower() for c in password)):
            okSmall = True
        if(any(c.isupper() for c in password)):
            okBig = True
        if(any(c.isnumeric() for c in password)):
            okDigit = True

        if(not(okSmall and okBig and okDigit)):
            return "Invalid password."
        return ""

#2 0 0 2 9 9 9 8 0 0 0 6 8

#a 0 b 1 c 2 d 3 e 4 f 5 g 6 h 7 i 8 j 9 k 10 l 11
#m = 11 − (( 7×(a + g) + 6×(b + h) + 5×(c + i) + 4×(d + j) + 3×(e + k) + 2×(f + l) ) mod 11)