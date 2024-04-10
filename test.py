import os

def delete_files_containing_word(directory, word):
    # iterate through the list of files in my directory
    for filename in os.listdir(directory):
        # check if the the specified word is exist in file names
        if word in filename:
            # joining the path + file name to delete it
            filepath = os.path.join(directory, filename)
            # check if the path + file name is actually exist
            if os.path.isfile(filepath):
                # remove the file
                os.remove(filepath)
                # print for debugging
                print(f'Deleted file: {filepath}')
# Example usage
directory_path = './static/'
word_to_search = 'try'
delete_files_containing_word(directory_path, word_to_search)