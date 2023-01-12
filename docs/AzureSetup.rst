#. Login to `Azure Lab Services <https://labs.azure.com/virtualmachines?feature_vnext=true>`_
#. If the virtual machine is not started, click the **start bubble**.

    .. image:: azureimages/Picture1.png

#. Once started, click the **computer icon** to get connection information.

    .. image:: azureimages/Picture2.png

#. Select **Connect via SSH**

    .. image:: azureimages/Picture3.png

#. Click **copy** to copy the ssh connection information.

    .. image:: azureimages/Picture4.png

#. **Install** X2Go client on your local computer. `Install X2Go <https://wiki.x2go.org/doku.php/doc:installation:x2goclient>`_

#. **Follow** the instructions on the website for your operating system.

#. **Open** X2Go and start a **new session** with Session, New Session.

    .. image:: azureimages/Picture5.png
 
#. **Change** the session name to what you prefer, example: HVOC

#. All the info you need is in the **copied** ssh connection information.

    * so, using **your** version of the info from step 5 you can find **host**, **login** and **port**.
    * say your 'copy' info is: ssh -p 5001 sysops@lab-d7054573-e093-4183-9a64-d2be946daa13.southcentralus.cloudapp.azure.com
  
    then:
  
    * The **host** is the computer name after the '@': **lab-d7054573-e093-4183-9a64-d2be946daa13.southcentralus.cloudapp.azure.com**
  
    * The **login** is the name immediately before the '@': **sysops**
  
    * The SSH **port** is the number after the '-p' flag: **5001**


#. Change the session type to **XFCE**

    .. image:: azureimages/Picture6.png

#. Click **OK**

#. Click on your **new session** and you will be propmted for a **password**.

#. Type in the password and select **OK**.

#. Select **Yes**.

#. Select **Yes**.
