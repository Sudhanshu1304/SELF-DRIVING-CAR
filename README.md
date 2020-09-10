# SELF_DRIVING-_CAR-



#### *LIBRARIES USED*

* Kivy
* PyTorch

### Sections

* About Kivy
* About PyTorch
* WHY PyTorch AND NOT ~~TensorFlow~~ ?


#### About Kivy

<img src="Images/kivy_img.png" width="10" height="10">

![](Images/kivy_img.png )

<p>

<br>

**Kivy** is a free and open source Python framework for 
developing mobile apps and other multitouch application 
software with a natural user interface. It is distributed under 
the terms of the MIT License,
 and can run on Android, iOS, GNU/Linux, macOS, and Windows

[Official Kivy Website Link ](https://kivy.org/#home)

</p>

### About PyTorch

![](Images/PyTorch.jpg)

<p>

**PyTorch** is an open source machine learning library based on the Torch library, 
used for applications such as computer vision and natural language processing,
 primarily developed by Facebook's AI Research lab.
 It is free and open-source software released under the Modified BSD license.

</p>

<br>

### Why PyTorch and Not TensorFlow ?
<br>

<p>
In my Opinion whenever we want to have control over the very fundamentals processes
link " Having the ability to to call the Back-Prop and Forward Propagation as and when required
 " This thing may be possible in TensorFlow But it Become too slow for such kind of a project.
 
 [Technical difference between TensorFlow and PyTorch on Quora](https://www.quora.com/Which-platform-is-the-best-to-build-a-self-driving-car-TensorFlow-PyTorch-or-Keras)


</p>

<br>

### Project Approach


[Kivy Link ](https://kivy.org/docs/tutorials/pong.html)

For The GUI Part The About Official Example of Kivy Implementation Helped 
a Lot  of It. In Fact Some of the Code Snippet's are so Fundamental That It
Provided Direct Help in Making this Project. 

For The GUI PART 

[Reinforcement Learning Link ](http://karpathy.github.io/2016/05/31/rl/)

The Above Link helped me a Lot In Understanding the Key Concepts and how to 
approach this  Project .


#### Concepts  Used  In Project

* The Very fundamental concept is about Exploration
> **It Is Very Important to know that Unlike in normal Supervised Learning Projects where 
>we have to give the give the correct solution of a particular Input ,here we Do not have any thing 
>before hand so for dealing with such Issue we have to Let the Car play Random Moves 
>and Let the Car To Explore the Environment and Gather Experience**


* Experience Memory

>**During the Exploration the Car gains Experience ,Practically it means that we have to
>store the Data Gained like the *Reward corresponding to a particular State*
>in a memory cell which can be made using the List Data Structure in Python.**

>**This Memory also has a very Important Role to play i.e Consider the Car is Trained 
>on the Input's of its Present State , Since we are Dealing with the Weights of the 
>Neural Network in the Back ,The Neural Network will soon forget the Experience It 
>had for the States it had been before because It's weights will adjusted it self to the new states it is in.**

>**This Means that the Car wil not learn effectively and every time it comes across the 
>same states as it have been before it will have to Explore that environment again, which makes no sense.
>**
>
>**So to deal with this Issue We Train out Neural Net on the Experiential Memory also
>so that the weights are not lost completely and helps in generalizing Car for Different
>Environments**






