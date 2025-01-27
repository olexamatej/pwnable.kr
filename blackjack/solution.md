### Task

`Hey! Check out this C implementation of a blackjack game!
I found it online
* http://cboard.cprogramming.com/c-programming/114023-simple-blackjack-program.html

I like to give my flags to millionaires.
How much money you got?

Running at : nc pwnable.kr 9009`

### Solution

After connecting to the server, we are placed into a blackjack game, the implementation of which is linked in the task description. Upon analyzing the code, we find a vulnerability in the betting logic:

```C
if(player_total < dealer_total) // If player's total is less than dealer's total, loss
{
    printf("\nDealer Has the Better Hand. You Lose.\n");
    loss = loss + 1;
    cash = cash - bet;
    printf("\nYou have %d Wins and %d Losses. Awesome!\n", won, loss);
    dealer_total = 0;
    askover();
}
```

The game prevents you from betting more than you have, but it allows you to bet a negative number (e.g., -99999999). If you lose the round, the negative bet will be subtracted from your cash - increasing your balance. This allows you to become a millionaire and retrieve the flag.