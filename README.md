# Huffman Encryptor
## How to Use this Website?
### Encrypt feature
This feature allows the user to upload a text file which after being put into my Huffman Encryption algorithm is fully encrypted. Then the new encrypted text file is returned as well as a key file in a compressed zip. The key file contains a binary tree with encoded values which will help the algorithm decode the file later.
### Decrypt feature
After the user encrypts the file they can use the Decrypt feature which takes the encrypted text file and key file as input and outputs the original text file.
## Build Process
During my Freshman year as a Computer Science student, I worked on a Huffman Compression algorithm as a part of my Data Structures class.
The thought of an algorithm that took the frequency of bit combinations and used it to compress files really fascinated me, but then I had the idea that this algorithm could not only be used to compress files but also encrypt them as well.
With this new idea in mind, I set out to implement it in website form. On the way to completion, I came across three challenges,
### 1. Which Language would I use?
I originally wrote my compression algorithm in Java but knew I wanted to turn this idea into a website and Java would not be the best language to use. I then moved to JavaScript but the lack of type-checking was causing issues in my coding process, which is when I decided to try out TypeScript.
After coding the encryption algorithm fully in TypeScript I began to have trouble handling files efficiently with the language which is when I decided to switch back to my old friend Python. Once I finished the algorithm in Python I ran into my next challenge.
### 2. Which Web Framework would I use?
The only Python web framework which I have had previous experience with is Django. I considered using Django for this project however I realized that it was unnecessarily heavy since this project only required a very simple backend and no database.
After realizing this I settled on using Flask as my framework of choice. Using Flask was very enjoyable and did feel like a lightweight version of Django with all the amenities I needed. After building the website in Flask I ran into my third and final challenge.
### 3. How would I deploy my project?
Since this website was not going to be static I could not use my default deployment method of choice which is Github Pages. I considered using methods such as Netlify and Heroku but settled for a new-to-me deployment method, PythonAnywhere. It was very easy to  set up and my first website is completely free to host.
