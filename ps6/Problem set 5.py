class Message(object):
    # ...existing code...

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        shift_dict = {}
        for i in range(26):
            shift_dict[string.ascii_lowercase[i]] = string.ascii_lowercase[(i + shift) % 26]
            shift_dict[string.ascii_uppercase[i]] = string.ascii_uppercase[(i + shift) % 26]
        return shift_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shift_dict = self.build_shift_dict(shift)
        encrypted_message = []
        for char in self.message_text:
            if char in shift_dict:
                encrypted_message.append(shift_dict[char])
            else:
                encrypted_message.append(char)
        return ''.join(encrypted_message)

# ...existing code...