import customtkinter as ctk
from buttons import Button, ImageButton, NumButton, MathButton
import darkdetect
from PIL import Image
from settings import *

class Calculator(ctk.CTk):
    def __init__(self, is_dark):
        
        #setup
        super().__init__(fg_color = (WHITE, BLACK))
        ctk.set_appearance_mode(f'{"dark" if is_dark else "light"}')
        self.title('')
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
        self.resizable(False, False)
        
        #grid layout
        self.rowconfigure(list(range(MAIN_ROWS)), weight=1, uniform='a')
        self.columnconfigure(list(range(MAIN_COLUMNS)), weight=1, uniform='a')
        
        #data
        self.result_string = ctk.StringVar(value='0')
        self.formula_string = ctk.StringVar(value='')
        self.display_nums = []
        self.full_operation = []
        
        #widgets
        self.create_widgets()

        self.mainloop()
    
    def create_widgets(self):
        #fonts
        main_font = ctk.CTkFont(family=FONT, size=NORMAL_FONT_SIZE)
        result_font = ctk.CTkFont(family=FONT, size=OUTPUT_FONT_SIZE)
        
        #Output Labels
        OutputLabel(self, 0, 'se', main_font, self.formula_string) #formula
        OutputLabel(self, 1, 'e', result_font, self.result_string) #result
        
        #clear (AC) button
        Button(
            parent=self,
            text = OPERATOR['clear']['text'],
            func = self.clear,
            col = OPERATOR['clear']['col'],
            row = OPERATOR['clear']['row'],
            font = main_font,
            )
        
        #percentage button
        Button(
            parent=self,
            text = OPERATOR['percent']['text'],
            func = self.percent,
            col = OPERATOR['percent']['col'],
            row = OPERATOR['percent']['row'],
            font = main_font,
            )
        
        #invert Button
        #invert_image = ctk.CTkImage(
            #light_image= Image.open(OPERATOR['invert']['image-path']['dark']), 
            #dark_image = Image.open(OPERATOR['invert']['image-path']['light'])
        #)
        Button(
            parent=self,
            text = OPERATOR['invert']['text'],
            func = self.invert,
            col = OPERATOR['invert']['col'],
            row = OPERATOR['invert']['row'],
            font = main_font,
            )
        
        #number buttons
        for num, data in NUM_POSITIONS.items():
            NumButton(
                parent = self,
                text = num,
                func = self.num_press,
                col = data['col'],
                row = data['row'],
                span = data['span'],
                font = main_font
            )
        
        #math buttons
        for operator, data in MATH_POSITIONS.items():
            MathButton(
                parent = self,
                text = data['character'],
                operator = operator,
                func = self.math_press,
                col = data['col'],
                row = data['row'],
                font = main_font
            )
    
    def num_press(self, value):
        self.display_nums.append(str(value))
        full_number = ''.join(self.display_nums)
        self.result_string.set(full_number)
    
    def math_press(self, value):
        current_number = ''.join(self.display_nums)
        
        if current_number:
            self.full_operation.append(current_number)
            
            if value != '=':
                #update data
                self.full_operation.append(value)
                self.display_nums.clear()
                
                #update output
                self.result_string.set('0')
                self.formula_string.set(' '.join(self.full_operation))
            else:
                formula = ' '.join(self.full_operation)
                result = eval(formula)

                #format the result
                if isinstance(result, float):
                    
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 3)
                
                #update the data
                self.full_operation.clear()
                self.display_nums = [str(result)]
                
                #update my output
                self.result_string.set(result)
                self.formula_string.set(formula)
                
    def clear(self):
        self.result_string.set('0')
        self.formula_string.set('')
        
        self.display_nums.clear()
        self.full_operation.clear()
    
    def percent(self):
        if self.display_nums:
            current_number = float(''.join(self.display_nums))
            percent_number = current_number / 100

            self.display_nums = list(str(percent_number))
            self.result_string.set(''.join(self.display_nums))
        
    def invert(self):
        current_number = ''.join(self.display_nums)
        if current_number:
            #positive / negative
            if float(current_number) > 0:
                self.display_nums.insert(0,'-')
            else:
                del self.display_nums[0]
            
            self.result_string.set(''.join(self.display_nums))
            
class OutputLabel(ctk.CTkLabel):
    def __init__(self, parent, row, anchor, font, string_var):
        super().__init__(master=parent, textvariable = string_var, font=font)
        
        self.grid(column = 0, columnspan = 4, row = row, sticky = anchor, padx = 10)
        
if __name__ == '__main__':
    Calculator(darkdetect.isDark())