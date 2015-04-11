#!/usr/bin/python
__author__ = 'Fernando Zhu'

import os
import sys
import getopt
import texttable
import platform
from random import randint

op_dict = {'AND': '001000',
        'OR': '001100',
        'ADD': '111000',
        'SUBV': '000011',
        'SUB': '000100',
        'LDR': '000000',
        'STR': '000010',
        'JMP': '011000',
        'PRESENT': '011100',
        'DCALLBL': '101000',
        'DCALLNB': '101001',
        'SZ': '010100',
        'CLFZ': '010000',
        'CER': '111100',
        'CEOT': '111110',
        'SEOT': '111111',
        'LER': '110110',
        'SSVOP': '111011',
        'LSIP': '110111',
        'SSOP': '111010',
        'NOOP': '110100',
        'MAX': '011110',
        'STRPC': '011101'}

am_dict = {'Inherent': '00',
        'Immediate': '01',
        'Direct': '10',
        'Register': '11'}



def greeting():

    asc1 = '''
    mm
 /^(  )^\  
 \,(..),/
   V~~V    -Hello
    '''
    
    # asc_list = (asc1, asc2);
    # print  asc_list[randint(0,2)]
    print asc1

    if platform.system() in ('Darwin', 'Linux'):
        print '\033[33m'
        print '#'*50
        print '#'*15, 'ReCOP Py-Compiler', '#'*16
        print '#'*15, 'Fernando Zhu', '#'*21
        print '#'*50
        print 
        print 'Usage Example: LDR Rz   #Operand'
        print '               LDR 0011 #0000000000000001 --Binary value'
        print '           or  LDR 0011 #d1               --Decimal value' 
        print '           or  LDR 0011 #x0001            --Hexadecimal value' 
        print '\033[0m'
    else:
        print '#'*50
        print '#'*15, 'ReCOP Py-Compiler', '#'*16
        print '#'*15, 'Fernando Zhu', '#'*21
        print '#'*50
        print 
        print 'Usage Example: LDR Rz   #Operand'
        print '               LDR 0011 #0000000000000001 --Binary value'
        print '           or  LDR 0011 #d1               --Decimal value' 
        print '           or  LDR 0011 #x0001            --Hexadecimal value' 
        print 


def main():
    machine_instruction = ''
    am = ''
    opcode = ''
    operand  = ''
    rx = '0000'
    rz = '0000'

    greeting()
    ins_table = texttable.Texttable()
    while True:
        ins_table.reset()
        ins_table.header(['Type', 'Binary','Hexadecimal'])
        ins_table.set_cols_dtype(['t', 't', 't'])
        ins_table.set_cols_align(['c', 'c', 'c'])

        asm_instruction = raw_input('\033[36mINSTRUCTION > \033[0m')
        if asm_instruction.lower() in ('quit', 'q'):
            break
        asm_instruction = asm_instruction.split()
        if asm_instruction[0].upper() not in [key for key in op_dict.keys()]:
            print 'Error: Please check your instruction again'
            sys.exit(0)
        if '#' in asm_instruction[len(asm_instruction) - 1]:
            # Immediate
            am = '01'
        elif '$' in asm_instruction[len(asm_instruction) - 1]:
            # Direct
            am = '10'
        elif len(asm_instruction) is 4 or len(asm_instruction) is 2 or asm_instruction[0].upper() in ('STR', 'LDR', 'LSIP' 'SSOP', 'DCALLNB', 'DCALLBL'): 
            # Register
            am = '11'
        elif  len(asm_instruction) is 1:
            am = '00'

        opcode = op_dict.get(asm_instruction[0].upper())

        
        if am is '01':
            operand = asm_instruction[len(asm_instruction)-1]
            for special_char in ('$', '#'):
                if special_char in operand:
                    operand = operand.replace(special_char, '')

            # The operand from user is decimal

            if 'd' in operand:
                operand = operand.replace('d', '')
                operand = format(int(operand), '016b')
               
            elif 'x' in operand:
                operand = operand.replace('x', '')
                if len(operand) is not 4:
                    print 'The width of operand is wrong, please check'
                    sys.exit(0);
                operand = format(int(operand, 16), '016b')
            else:
                if len(operand) is not 16:
                    print 'The width of operand is wrong, please check'
                    sys.exit(0);


                print 'decimal'
            if len(asm_instruction) is 4:
                rz = asm_instruction[1]
                rx = asm_instruction[2]
            elif len(asm_instruction) is 3:
                rz = asm_instruction[1]
                # rx = 'xxxx'
                rx = '0000'
            elif len(asm_instruction) is 2 and (asm_instruction[0].upper() == 'JMP'):
                rz = '0000'
                rx = '0000'
        elif am is '10':
            operand = asm_instruction[len(asm_instruction)-1]
            for special_char in ('$', '#'):
                if special_char in operand:
                    operand = operand.replace(special_char, '')

            if asm_instruction[0].upper() is 'LDR':
                rz = asm_instruction[1]
                #rx = 'xxxx'
                rx = '0000'
            elif asm_instruction[0].upper() is 'STR':
                rz = 'xxxx'
                rx = asm_instruction[1]
            elif asm_instruction[0].upper() is 'STRPC':
                #rz = 'xxxx'
                #rx = 'xxxx'
                rz = '0000'
                rx = '0000'
        elif am is '11':
            operand = '0000000000000000'
            if len(asm_instruction) is 4:
                rz = asm_instruction[1]
                rx = asm_instruction[3]
            elif len(asm_instruction) is 3:
                rz = asm_instruction[1]
                rx = asm_instruction[2]
            elif len(asm_instruction) is 2:
                if asm_instruction[0].upper() in ['LER', 'LSIP']:
                    rz = asm_instruction[1]
                    # rx = 'xxxx'
                    rx = '0000'
                else:
                    # rz = 'xxxx'
                    rz = '0000'
                    rx = asm_instruction[1]

        elif am is '00':
            rz = '0000'
            rx = '0000'

            operand = '0000000000000000'
                
        if len(am) is not 2:
            print 'The width of addressing mode is wrong, please check'
            sys.exit(0);
        if len(opcode) is not 6:
            print 'The width of opcode is wrong, please check'
            sys.exit(0);
        if len(rz) is not 4:
            print 'The width of rz is wrong, please check'
            sys.exit(0);
        if len(rx) is not 4:
            print 'The width of rz is wrong, please check'
            sys.exit(0);
        
        color_machine_instruction = '\033[31m' + am + '\033[32m'  + opcode + '\033[33m'+ rz + '\033[36m'+ rx + '\033[0m'
        color_operand = '\033[35m'+ operand +  '\033[0m'
        machine_instruction = am + opcode + rz + rx 
        
        machine_instruction_hex = hex(int(machine_instruction, 2))
        machine_operand_hex = hex(int(operand, 2))
        if len(machine_operand_hex) < 6:
            machine_operand_hex = machine_operand_hex[:2] + '0'*(6 - len(machine_operand_hex)) + machine_operand_hex[2:]
        if len(machine_instruction_hex) < 6:
            machine_instruction_hex = machine_instruction_hex[:2] + '0'*(6 - len(machine_instruction_hex)) + machine_instruction_hex[2:]


        '''
        print 'instruction width: %d' % len(machine_instruction)
        print 'am ' + am, ' %d' % len(am)
        print 'opcode ' + opcode, ' %d' % len(opcode)
        print 'rz ' + rz, ' %d' % len(rz)
        print 'rx ' + rx, ' %d' % len(rx)
        print 'operand ' + operand, ' %d' % len(operand)
        '''
        
        ins_table.add_row(['Instruction', machine_instruction, machine_instruction_hex])
        ins_table.add_row(['Operand', operand, machine_operand_hex])

        print 'Instruction + Operand (32bits) --> '
        if platform.system() in ('Darwin', 'Linux'):
            print ' '*15 + color_machine_instruction,  color_operand

        else: 
            machine_instruction = am +' '+ opcode +' '+ rz +' '+ rx 
            print machine_instruction, ' '*2 , operand
                

        print ins_table.draw()
       
if __name__ == '__main__':
    main()
