##############################################################################
# COMPONENT:
#    CIPHER01
# Author:
#    Br. Helfrich, Kyle Mueller, <your name here if you made a change>
# Summary:
#    Implement your cipher here. You can view 'example.py' to see the
#    completed Caesar Cipher example.
##############################################################################

#############################################################################
# IMPORTED LIBRARIES
#############################################################################
import math

##############################################################################
# CIPHER
##############################################################################
class Cipher:
    def __init__(self):
        self.padding_character = "\0"
        pass

    def get_author(self):
        return "Kimberly Uresti"

    def get_cipher_name(self):
        return "Columnar Transposition"

    ##########################################################################
    # GET CIPHER CITATION
    # Returns the citation from which we learned about the cipher
    ##########################################################################
    def get_cipher_citation(self):
        s =  "Adyapak, N. M., B, V., & B, P. H. (2022), " \
             "\"A Novel Way of Decrypting Single Columnar Transposition Ciphers,\" " \
             "\n   2022 International Conference on Smart Generation Computing, " \
             "Communication and Networking (SMART GENCON), pp. 1-8, DOI: " \
             "https://doi.org/10.1109/SMARTGENCON56628.2022.10083631" \
             "\n\n" \
             
        s += "Al-Sabaawi, A. (2021), " \
             "\"Cryptanalysis of Classic Ciphers: Methods Implementation Survey,\" " \
             "\n   2021 International Conference on Intelligent Technologies (CONIT), " \
             "pp. 1-6, DOI: " \
             "https://doi.org/10.1109/CONIT51480.2021.9498530"

        return s

    ##########################################################################
    # GET PSEUDOCODE
    # Returns the pseudocode as a string to be used by the caller
    ##########################################################################
    def get_pseudocode(self):
        # TODO: This function should return your psuedocode, neatly formatted

        # The encrypt pseudocode
        pc = "encrypt(plainText, password)\n" \
             "   numberOfColumns <- length of password\n" \
             "   messageLength <- length of plainText\n" \
             "   numberOfRows <- ceiling(messageLength / numberOfColumns)\n" \
             "   emptyCells <- (numberOfRows * numberOfColumns) - messageLength\n" \
             "   FOR count <- 1 TO emptyCells\n" \
             "      plainText <- plainText + paddingCharacter\n" \
             "   matrix <- empty matrix with numberOfRows rows and numberOfColumns columns\n" \
             "   textIndex <- 0\n" \
             "   FOR row <- 0 TO numberOfRows - 1\n" \
             "      FOR column <- 0 TO numberOfColumns - 1\n" \
             "         matrix[row][column] <- plainText[textIndex]\n" \
             "         textIndex <- textIndex + 1\n" \
             "   keyOrder <- columnOrder(password)\n" \
             "   cipherText <- empty string\n" \
             "   FOR keyNumber <- 1 TO numberOfColumns\n" \
             "      columnIndex <- position of keyNumber in keyOrder\n" \
             "      FOR row <- 0 TO numberOfRows - 1\n" \
             "         cipherText <- cipherText + matrix[row][columnIndex]\n" \
             "   encryptedMessage <- messageLength + \":\" + cipherText\n" \
             "   RETURN encryptedMessage and original message length\n\n"
            

        # The decrypt pseudocode
        pc += "decrypt(encryptedMessage, password)\n" \
              "   numberOfColumns <- length of password\n" \
              "   messageLengthText, cipherText <- split encryptedMessage at first \":\"\n" \
              "   messageLength <- convert messageLengthText to integer\n" \
              "   numberOfRows <- length of cipherText / numberOfColumns\n" \
              "   matrix <- empty matrix with numberOfRows rows and numberOfColumns columns\n" \
              "   keyOrder <- columnOrder(password)\n" \
              "   cipherTextIndex <- 0\n" \
              "   FOR keyNumber <- 1 TO numberOfColumns\n" \
              "       columnIndex <- position of keyNumber in keyOrder\n" \
              "       FOR row <- 0 TO numberOfRows\n" \
              "           matrix[row][columnIndex] <- cipherText[cipherTextIndex]\n" \
              "           cipherTextIndex <- cipherTextIndex + 1\n" \
              "   paddedPlainText <- empty string\n" \
              "   FOR row <- 0 TO numberOfRows - 1\n" \
              "       FOR column <- 0 TO numberOfColumns - 1\n" \
              "           paddedPlainText <- paddedPlainText + matrix[row][column]\n" \
              "   plainText <- first messageLength characters of paddedPlainText\n" \
              "   RETURN plainText\n\n"

        # Helper routine
        pc += "create_key_order(password)\n" \
              "   passwordCharacters <- empty list\n" \
              "   FOR position <- 0 to length of password - 1\n" \
              "       ADD password[position] and position to passwordCharacters\n" \
              "   SORT passwordCharacters by character value\n" \
              "   KEEP duplicate characters in their original position order\n" \
              "   keyOrder <- list of zeros with length of password\n" \
              "   rank <- 1\n" \
              "   FOR EACH storedCharacter IN passwordCharacters\n" \
              "      originalPosition <- storedCharacter's original position\n" \
              "      keyOrder[originalPosition] <- rank\n" \
              "      rank <- rank + 1\n" \
              "   RETURN keyOrder\n\n"

        return pc

    ##########################################################################
    # ENCRYPT
    # Rearranges the plaintext into password-ordered columns and returns the
    # resulting ciphertext with the original message length.
    ##########################################################################
    def encrypt(self, plaintext, password):

        # Get the number of columns according to the password
        # Then use the no. of columns to determine number of rows
        number_of_columns = len(password)
        original_length = len(plaintext)

        number_of_rows = math.ceil(original_length / number_of_columns)

        # Determine the amount of padding needed to fill
        # all the rows.
        padded_length = number_of_rows * number_of_columns
        padding_needed = padded_length - original_length

        padded_plaintext = plaintext + (self.padding_character * padding_needed)

        # Build the matrix of columns and rows
        matrix = []

        for position in range(0, padded_length, number_of_columns):
            row = padded_plaintext[
                position:position + number_of_columns
            ]
            matrix.append(list(row))

        # Use the password to determine the order of encryption
        # Populate the ciphertext one character at a time in the
        # order determined from the password.
        key_order = self.create_key_order(password)
        ciphertext = ""
        
        for key_number in range(1, number_of_columns + 1):
            column_index = key_order.index(key_number)

            for row in matrix:
                ciphertext += row[column_index]
        
        # Returns original_length, to be used in the decrypt function,
        # and the resulting ciphertext.
        return f"{original_length}:{ciphertext}"

    ##########################################################################
    # DECRYPT
    # Reconstructs the original plaintext by re-ordering the encrypted columns
    # according to the order derived from the password.
    ##########################################################################
    def decrypt(self, encrypted_message, password):
        plaintext = encrypted_message
       
       # Get the number of columns according to password length
       # Get the number of rows by using the original_length
        number_of_columns = len(password)

        length_text, ciphertext = encrypted_message.split(":", 1)
        original_length = int(length_text)

        number_of_rows = len(ciphertext) // number_of_columns

        # Determine the key_order with the password
        key_order = self.create_key_order(password)

        # Build the matrix with the number_of_columns and number_of_rows
        matrix = []

        for _ in range(number_of_rows):
            empty_row = [""] * number_of_columns
            matrix.append(empty_row)

        # Using the key_order populate the matrix with the ciphertext
        # characters into columns in the order the password dictates.
        # Removes any padding and returns the decrypted message
        ciphertext_position = 0

        for key_number in range(1, number_of_columns + 1):
            column_index = key_order.index(key_number)

            for row_index in range(number_of_rows):
                matrix[row_index][column_index] = (
                    ciphertext[ciphertext_position]
                )
                ciphertext_position += 1

        plaintext = ""

        for row in matrix:
            plaintext += "".join(row)

        return plaintext[:original_length]

    ##########################################################################
    # HELPER ROUTINE : CREATE_KEY_ORDER
    # Takes the password then sorts and ranks each character to create
    # the key_order used to encrypt and decrypt texts
    ##########################################################################
    def create_key_order(self, password):

        # Characters of the password are set to an numbered list
        password_characters = list(enumerate(password))

        # Sorts the password characters according to two values, order value (the Unicode
        # value for the character) and the character's original position. This
        # allows letters, digits, spaces, and symbols while also handling duplicate
        # characters by tracking which character was first.
        sorted_characters = sorted(
            password_characters,
            key=lambda item: (ord(item[1]), item[0])
        )

        # Creates an empty list to store the key_order result
        key_order = [0] * len(password)

        # This loop ranks the sorted_characters starting with 1
        for rank, (original_index, _) in enumerate(
            sorted_characters,
            start=1
        ):
            # Each rank is then put into its original character position.
            key_order[original_index] = rank
        
        return key_order