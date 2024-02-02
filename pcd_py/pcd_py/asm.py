import os

class Assembler():
    def __init__(self, *args):
        # Instructions and their opcode

        self.opCodes = { 'NOP':'0',  'BNK':'1',  'OUT':'2',  'CLC':'3',  'SEC':'4',  'LSL':'5',  'ROL':'6',  'LSR':'7',
            'ROR':'8',  'ASR':'9',  'INP':'10', 'NEG':'11', 'INC':'12', 'DEC':'13', 'LDI':'14', 'ADI':'15',
            'SBI':'16', 'CPI':'17', 'ACI':'18', 'SCI':'19', 'JPA':'20', 'LDA':'21', 'STA':'22', 'ADA':'23',
            'SBA':'24', 'CPA':'25', 'ACA':'26', 'SCA':'27', 'JPR':'28', 'LDR':'29', 'STR':'30', 'ADR':'31',
            'SBR':'32', 'CPR':'33', 'ACR':'34', 'SCR':'35', 'CLB':'36', 'NEB':'37', 'INB':'38', 'DEB':'39',
            'ADB':'40', 'SBB':'41', 'ACB':'42', 'SCB':'43', 'CLW':'44', 'NEW':'45', 'INW':'46', 'DEW':'47',
            'ADW':'48', 'SBW':'49', 'ACW':'50', 'SCW':'51', 'LDS':'52', 'STS':'53', 'PHS':'54', 'PLS':'55',
            'JPS':'56', 'RTS':'57', 'BNE':'58', 'BEQ':'59', 'BCC':'60', 'BCS':'61', 'BPL':'62', 'BMI':'63'  }

        self.lines, self.lineinfo, self.lineadr, self.labels = [], [], [], {}
        self.LINEINFO_NONE, self.LINEINFO_ORG, self.LINEINFO_BEGIN, self.LINEINFO_END = 0x00000, 0x10000, 0x20000, 0x40000

        import sys # read in <source file> 2nd command parameter line by line
        if len(sys.argv) != 2: print("usage: asm.py <sourcefile>"); sys.exit(1)
        f = open(sys.argv[1], 'r')
        while True: # read in the source line
            line = f.readline()
            if not line: break
            self.lines.append(line.strip()) # store each line without leading or trailing whitespaces
        f.close()

        for i in range(len(self.lines)):    # pass 1: do per line replacements
            while(self.lines[i].find('\'') != -1):  # replace '...' occurances with corresponding ASCII codes
                k = self.lines[i].find('\'')
                l = self.lines[i].find('\'', k+1)
                if k != -1 and l != -1:
                    replaced = ''
                    for c in self.lines[i][k+1:l]: replaced += str(ord(c)) + ' '
                    self.lines[i] = self.lines[i][0:k] + replaced + self.lines[i][l+1:]
                else: break

            if (self.lines[i].find(";") != -1): self.lines[i][0:self.lines[i].find(";")]    # delete commants
            self.lines[i] = self.lines[i].replace(",", " ") # replace commas with spaces

            self.lineinfo.append(self.LINEINFO_NONE)    # generate a seperate lineinfo
            if self.lines[i].find("#begin") != -1: self.lineinfo[i] |= self.LINEINFO_BEGIN; self.lines[i] = self.lines[i].replace("#begin", "")
            if self.lines[i].find("#end") != -1: self.lineinfo[i] |= self.LINEINFO_END; self.lines[i].replace("#end", "")
            k = self.lines[i].find("#org")
            if (k != -1):
                s = self.lines[i][k:].split()   # split form #org onwards
                self.lineinfo[i] |= self.LINEINFO_ORG + int(s[1], 0)    # use element after #org as origin address
                self.lines[i] = self.lines[i][0:k].join(s[2:])  # oin everything before and after the #org ... statement

            if self.lines[i].find(":") != -1:
                self.labels[self.lines[i][:self.lines[i].find(":")]] = i    # store label with it's line number in dict
                self.lines[i] = self.lines[self.lines[i].find(':')+1:]  # cut out the label

            self.lines[i] = self.lines[i].split()   # now split line into list of bytes (omitting whitespaces)

            for j in range(len(self.lines[i]) -1, -1, -1):  # iterate from back to front while inserting stuff
                try: self.lines[i][j] = self.opCodes[self.lines[i][j]]  # try replacing mnemonic with opcode
                except:
                    if self.lines[i][j].find("0x") == 0 and len(self.lines[i][j]) > 4:  # replace '0xword' with 'LSB MSB'
                        val = int(self.lines[i][j], 16)
                        self.lines[i][j] = str(val & 0xff)
                        self.lines[i].insert(j+1, str((val>>8) & 0xff))

        adr = 0 # pass 2: default start address
        for i in range(len(self.lines)):
            for j in range(len(self.lines[i]) -1, -1, -1):      # iterate from back to front while insterting stuff
                e = self.lines[i][j]
                if e[0] == '<' or e[0] == '>': continue # only one byte is required for this label
                if e.find("+") != -1: e = e[0:e.find("+")]  # omit + or - expressions  after a label
                if e.find('-') != -1: e = e[0:e.find('-')]
                try:
                    self.labels[e]; self.lines[i].insert(j+1, '0x@@')   # is this element a label? => add a placeholder for MSB
                except: pass
            if self.lineinfo[i] & self.LINEINFO_ORG: adr = self.lineinfo[i] & 0xffff    # react to #org by resetting the address
            self.lineadr.append(adr);   # save line start address
            adr += len(self.lines[i])   #advance address by number or byte elements

        for l in self.labels: self.labels[l] = self.lineadr[self.labels[l]] # update label dict from 'line number ' to 'address'

        for i in range(len(self.lines)):    # pass 3: replace 'reference + placeholder' with 'MSB LSB'
            for j in range(len(self.lines[i])):
                e = self.lines[i][j]; pre = ''; off = 0
                if e[0] == "<" or e[0] == ">": pre = e[0]; e=e[1:]
                if e.find("+") != -1: off += int(e[e.find("+")+1:], 0); e = e[0:e.find("+")]
                if e.find("-") != -1: off -= int(e[e.find("-")+1:], 0); e = e[0:e.find("-")]
                try:
                    adr = self.labels[e] + off
                    if pre == "<": self.lines[i][j] = str(adr & 0xff)
                    elif pre == ">": self.lines[i][j] = str((adr>>8) & 0xff)
                    else: self.lines[i][j] = str(adr & 0xff); self.lines[i][j+1] = str((adr>>8) & 0xff)
                except: pass
                try: int(self.lines[i][j], 0)   # check if all expression are numeric
                except: print("ERROR in line "+ str(i+1)+": Undefined expression \'" + self.lines[i][j] + '\''); exit(1)

        for i in range(len(self.lines)):    # print out the result
            s = ('%04.4x' % self.lineadr[i]) + ": "
            for e in self.lines[i]: s += ('%02.2x' % (int(e, 0) & 0xff)) + " "
            print(s)

TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MULT = "MULT"
TT_DIVIDE = "DIVIDE"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"

DIGITS = "0123456789"

class AOL_Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_str(self):
        result = f'{self.error_name}: {self.details}'
        result += f' File {self.pos_start.fn}, line  {self.pos_start.ln + 1}'
        return result

class AOL_ICError(BaseException):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(details)
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.details = details

    def as_str(self):
        result = f'Illegal Character: {self.details}'
        result += f' File {self.pos_start.fn}, line  {self.pos_start.ln + 1}'
        return result

class AOL_ISError(AOL_Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

class AOL_Tokens:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

class AOL_Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        if self.idx != None and self.ln != None and self.col != None:
            if current_char is not None:
                if current_char.isalnum() or current_char in "+-*/()":
                    self.idx += 1
                    self.col += 1

                    if current_char == "\n":
                        self.ln += 1
                        self.col = 0

                    return self
                else:
                    raise AOL_ICError(self.copy(), self.copy(), f"Unexpected character: '{current_char}'")

    def copy(self):
        return AOL_Position(idx=self.idx, ln=self.ln, col=self.col, fn=self.fn, ftxt=self.ftxt)

class AOL_EXTRA():
    def __init__(self, tok=None):
        self.tok = tok

    def NumberNode_repr(self):
        return f'{self.tok}'

    def BinOpNode(self, left_node, op_tok, right_node):
        return f'INT:{left_node} OPERATOR: {op_tok.type} INT:{right_node}'

    def ParserResult(self, mode="__init__", res=None, node=None, error=None):
        error = None
        node = None

        if mode == "register":
            if isinstance(res, AOL_EXTRA) and isinstance(res.ParserResult, type):
                if res.error: error = res.error
                return res.node

            return res

        elif mode == "success":
            node = node
            return node, error
        elif mode == "failure":
            error = error
            return error, node
        elif mode == "__init__":
            pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = 0  # Initialize the token index
        self.current_token = self.tokens[self.tok_idx] if self.tok_idx < len(self.tokens) else None
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_token = self.tokens[self.tok_idx]
        return self.current_token


    def parse(self):
        res = self.expr()
        return res

    def factor(self):
        res = AOL_EXTRA()
        tok = self.current_token

        if not tok == None and tok.type in (TT_INT, TT_FLOAT):
            res.ParserResult(mode="register", res=self.advance())
            return AOL_EXTRA(tok).NumberNode_repr()

    def term(self):
        return self.bin_op(self.factor, (TT_DIVIDE, TT_MULT))

    def expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def bin_op(self, func, ops):
        left = func()

        while not self.current_token == None and self.current_token.type in ops:
            op_tok = self.current_token
            self.advance()
            right = func()
            left = AOL_EXTRA().BinOpNode(left, op_tok, right)

        return left

class NoCurrentCharacterError(Exception):
    def __init__(self, message="AOL Error: No Current Character (Token) Found!"):
        self.message = message
        super().__init__(self.message)

class AOL_Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = AOL_Position(idx=-1, ln=0, col=-1, fn=fn, ftxt=text)
        self.current_char = None
        self.advance()

    def advance(self):
        while self.pos.idx < len(self.text) and (self.current_char is None or self.current_char.isspace()):
            print(f"Advancing position: {self.pos.idx}")
            self.pos.advance(self.current_char)
            if self.pos.idx < len(self.text):
                self.current_char = self.text[self.pos.idx]
            else:
                self.current_char = None

        while self.current_char is not None and self.current_char.isdigit():
            print(f"Inside make_number loop: {self.current_char}")
            self.pos.advance(self.current_char)
            if self.pos.idx < len(self.text):
                self.current_char = self.text[self.pos.idx]
            else:
                self.current_char = None

        print(f"New current_char: {self.current_char}")

    def make_Tokens(self):
        tokens = []

        if self.current_char is None:
            raise Exception("AOL Error: No Current Character (Token) Found!")

        tok = self.make_number()
        print(f"Entering make_Tokens: {tok}")

        while tok is not None:
            print(f"Inside make_Tokens loop: {tok}")
            if isinstance(tok, AOL_Tokens):
                if tok is not None and tok.type in (TT_INT, TT_FLOAT):
                    tokens.append(tok)
                elif tok is not None and tok.type == TT_PLUS:
                    tokens.append(AOL_Tokens(TT_PLUS))
                elif tok is not None and tok.type == TT_MINUS:
                    tokens.append(AOL_Tokens(TT_MINUS))
                elif tok is not None and tok.type == TT_MULT:
                    tokens.append(AOL_Tokens(TT_MULT))
                elif tok is not None and tok.type == TT_DIVIDE:
                    tokens.append(AOL_Tokens(TT_DIVIDE))
                elif tok is not None and tok.type == TT_LPAREN:
                    tokens.append(AOL_Tokens(TT_LPAREN))
                elif tok is not None and tok.type == TT_RPAREN:
                    tokens.append(AOL_Tokens(TT_RPAREN))
                else:
                    pos_start = self.pos.copy()
                    char = self.current_char
                    self.advance()
                    return [], AOL_ICError(pos_start, self.pos, "'" + char + "'")

            tok = self.make_number()
            print(f"New tok: {tok}")

        print("Exiting make_Tokens")
        return tokens, ""

    def make_number(self):
        num_str = ''
        dot_count = 0

        print("Entering make_number:", self.current_char)

        while self.current_char is not None and self.current_char in DIGITS + ".":
            print("Inside make_number loop:", self.current_char)
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        print("Exiting make_number:", num_str)

        if not num_str:
            return None  # Return None if no valid number was found

        if dot_count == 0:
            return AOL_Tokens(TT_INT, int(num_str))
        else:
            return AOL_Tokens(TT_FLOAT, float(num_str))

def AOL_run_start(file=None, fn="<asm.py>", asm_fn=None, mode="--file", text=None):
    if mode == "--file" and file != None:
        global content

        if os.path.exists(file) and os.path.isfile(file):
            with open(file, 'r') as file:
                file.seek(0)
                content = file.read()

            fn = '<'+ file[file.rfind("//") + 1:] + ">"

            lexer = AOL_Lexer(fn, content)
            tokens, error = lexer.make_Tokens()
            if error: return None, error
            parser = Parser(tokens)
            ast = parser.parse()
            return ast, None
    elif mode == "--console --interpreter":
        lexer = AOL_Lexer(fn, text)
        tokens, error = lexer.make_Tokens()
        if error: return None, error
        parser = Parser(tokens)
        ast = parser.parse()
        return ast, None
    else: print("No such mode")

def AOL_run(file=None, file_name=None, asm_file_name=None, mode="--console --interpreter"):
    if mode == "--console --interpreter":
        while True:
            text = input("AOL -> ")

            if text == "exit()": break

            result, error = AOL_run_start(text=text, mode="--console --interpreter")

            if error: print(error.as_str())
            else: print(result)
    elif mode == "--file":
        AOL_run_start(file=file, fn=file_name, asm_fn=asm_file_name, mode="--file")
    else: print("No such mode")

AOL_run(mode="--console --interpreter")