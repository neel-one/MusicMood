

def generate(in_file, out_file):
    with open(out_file, 'w') as of:
        for line in open(in_file):
            for word in line.split():
                of.write(word.lower() + '\n')



if __name__ == "__main__":
    
    generate('words.txt', 'word_list.txt')