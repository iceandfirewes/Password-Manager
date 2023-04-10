This is a desktop application that manages passwords. It asks the user for a master key, for example "ghana231", hash it and then finally use the hashed key for an AES encryption
Here are a few screenshot
![image](https://user-images.githubusercontent.com/49576270/226635892-18b31d8d-9e19-4d61-a685-34fe16907494.png)
![image](https://user-images.githubusercontent.com/49576270/230812004-60dbe528-3929-4768-8cef-b015bdf1f4f4.png)
Disclamer: 
  1. The .exe will be flagged and remove by window defender, user need to be exclude the .exe file in the window defender setting. I believe it is because of the program
    use of os.remove() to manage metadata.
  2. The program display the AES nonce and tags publicly in a .dat file. I do not know how insecure that is but from what I read, it not a breach of security.
  3. Once the masterkey has been set, you cannot change it without removing all passwords in the .dat files with the "Reset" button.
