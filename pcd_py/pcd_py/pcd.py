import os
import re
import pickle
import sqlparse

__all__ = ['Pcd_line']

class _MemorySaver():
    def __init__(self, table:dict='', tableName:str=''):
        self.table = table
        self.tableName = tableName
        self.file = ""

    def Exists(self, path):
        return os.path.exists(path)

    def save(self):
        if self.Exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "MemorySave")):
            with open(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MemorySave'), self.tableName+".pkl"), "wb") as file:
                pickle.dump(self.table, file)
        else:
            os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MemorySave'))
            self.save()

    def load(self):
        if self.Exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "MemorySave")):
            with open(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MemorySave'), self.tableName+".pkl"), "rb") as file:
                self.file = pickle.load(file)
        else:
            _Error("Could not find the 'MemorySave' directory", "File Not Found", "PCD.MemorySave", FileNotFoundError)
        return self.file

    def destroy(self):
        os.remove(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "MemorySave"), self.tableName+".pkl"))

class _Parser(): #Parser
    @staticmethod
    def Parse(query:str):
        parsed_dict = {}
        mode = None
        parsed = sqlparse.parse(query)
        stmt = parsed[0]  # Assuming a single SQL statement in the query
        tokens__ = []

        for v in stmt.tokens:
            if v.ttype == sqlparse.tokens.Whitespace or v.ttype == sqlparse.tokens.Wildcard:
                pass
            else:
                tokens__.append(v)

        for i, token in enumerate(tokens__):
            print(token)
            if token.value.upper() in ["SELECT", "ORDER BY", "FROM", "WHERE"]:
                if token.value.upper() == "SELECT":
                    parsed_dict.setdefault("SELECT", []).append(tokens__[i+1].value)
                elif token.value.upper() == "FROM":
                    parsed_dict.setdefault("FROM", tokens__[i+1].value)
                elif token.value.upper() == "WHERE":
                    parsed_dict.setdefault("WHERE", []).append(tokens__[i+1].value)

        return parsed_dict

class _PPCD():
    def __init__(self, table:dict={}, name:str="untitled", format:str=".ppcd", path:str=os.getcwd(), query:str='', *args):
        av_Format = [".ppcd", ".txt", ".psaf"]
        if not format in av_Format:
            _Error(f'Invalid Format [{format}] given', 'Format Error')
        self.format = format
        self.av_format = av_Format
        self.name = name
        self.table = table
        self.query = query
        if not os.path.exists(path):
            _Error("Could not find file", "File Error", Error=OSError)
        self.path = path
        self.file = self.name+self.format

    def UTable(self, mode:str="create", lines_:str="", *args): #Understand Table and return a string if mode is Create
        if mode == "create":
            base_str = ""
            for header, lines in self.table.items():
                base_str += f"[{header}]\n"
                for line in lines:
                    base_str += f"{line}\n"
                base_str += ";\n"
            return base_str
        elif mode == "read":
            current_header = None
            for line_ in lines_:
                line_ = line_.strip()
                if line_.startswith("[") and line_.endswith("]"):
                    current_header = line_[1:-1]  # Extracting "Row" or "Column"
                elif line_.startswith("$"):
                    self.table[current_header].append(line_)

            return self.table

    def Create(self): #Create file
        with open(os.path.join(self.path, self.file), "w") as ppcd:
            ppcd.write(self.UTable())
        print("Done Creating!")

    def Read(self): #Read file
        with open(os.path.join(self.path, self.file), "r") as ppcd:
            ppcd.seek(0)
            lines = ppcd.readlines() #Read lines
            return self.UTable(mode="read", lines_=lines)

    def Query(self): #Query function
        return self.UTable(mode="query")

class _Error(BaseException):
    def __init__(self, details:str='You cannot add alphabetical characters in Row or Column', message:str='Numeric Value Only', host:str='PCD', Error:BaseException=ValueError):
        raise Error(f"{host} Error: {message} \n {details}")

class Pcd_line():
    def __init__(self, mode:str="--terminal --format: .ppcd", *args):
        MODregex = re.compile(r"--(?P<mode>\w*)\s*--format:\s*.(?P<format>\w*)")
        match = MODregex.search(mode)
        self.mode = ""
        self.format = ""
        if match:
            self.mode = match.group('mode')
            self.format = "."+match.group('format')
        self.modes = ['terminal', 'script', 'aol', 'aos']
        self.formats = [".ppcd", ".psaf", ".txt"]
        if not self.format in self.formats:
            _Error(f"Invalid format given [{self.format}]. Only these {self.formats} formats are available.", "Invalid Format")
        elif not self.mode in self.modes:
            _Error(f"Invalid mode given [{self.mode}]. Only these {self.modes} modes are available.", "Invalid Mode")

    def _CreateAddress(self, val: str, str_: list, address:str=None, *args):
        addr = val.lower()+"0" #address for Value
        idx = 0
        while any(addr in s for s in str_):
            idx += 1
            addr = val.lower() + str(idx)  #Create simple Address

        if address: # replace address if it already exists
            addr = address
        return addr

    def _process_line(self, queries:list): #Process queries
        parser = _Parser()

        for query in queries:
            if "SELECT" in query.upper():
                result = parser.Parse(query)
                print(f"Query: {query}")
                print(f"Query Result: {result}")
            elif "INSERT" in query.upper():
                # Handle other types of queries
                pass
            else:
                _Error(f"Invalid Query - [{query}]", "Invalid Query")
    def run(self, query:str=""):
        queries = []
        if self.mode == "terminal":
            while True:
                query = input("Query: ") # Get Query
                if query.lower() == "stop$":
                    break
                queries.append(query)
            self._process_line(queries)
        elif self.mode == "script":
            queries.append(query) # Append Queries
            self._process_line(queries) # Run Query

Pcd_line().run()