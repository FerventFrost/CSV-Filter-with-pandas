# Queue maxsize doesn't work
code runs fine till the queue is full, Queue(maxsize = 3)

![image](https://user-images.githubusercontent.com/90336445/170888238-865b1654-befc-46fb-9664-500bc85dbc35.png)

![image](https://user-images.githubusercontent.com/90336445/170888281-dcc68410-37c3-4a0c-809c-df735b042e79.png)

i am trying to find a solution now


## Solution
i accidentally add parentheses in thread initialization.

![image](https://user-images.githubusercontent.com/90336445/170888710-15e8c312-4712-41d8-b66f-97e9cd20a492.png)

After removing it, it should work.

![image](https://user-images.githubusercontent.com/90336445/170889021-5fbc90df-9a81-405c-bfb0-4d42baef4e90.png)


![image](https://user-images.githubusercontent.com/90336445/170888818-247e2488-5647-479c-bca8-d0bea4bffa94.png)

Finally, so please keep an eye on these silly typos.
