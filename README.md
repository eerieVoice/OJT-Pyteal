# ABOUT THIS PROJECT

## TIC TAC TOE ALGORAND

### This project is about a pyteal smart contract for a simple tic tac toe game using two local state variables.

The smart contract has front end component inorder to interact with the smart contract.

```bash
https://github.com/eerieVoice/OJT-frontend.git
```

App.localPut(Txn.sender(),Bytes('ScoreX'), Int(0)): This instruction sets the value of the ScoreX local state variable for the current transaction sender to 0. The Bytes function is used to convert the string 'ScoreX' to bytes.

Return(Int(1)): This instruction returns a success value of 1 to indicate that the operation was successful.

```python

handle_creationX = Seq([
    App.localPut(Txn.sender(),Bytes('ScoreX'), Int(0)),  #uint64
    Return(Int(1))
    ])
    handle_creationO = Seq([
    App.localPut(Txn.sender(),Bytes('ScoreO'), Int(0)),  #uint64
    Return(Int(1))
    ])

```

Player1.store(App.localGet(Txn.sender(), Bytes('ScoreX'))): This instruction loads the current value of the ScoreX local state variable for the transaction sender and stores it in the scratch space of the contract using the label Player1.

App.localPut(Txn.sender(), Bytes('ScoreX') , Player1.load() + Int(1)): This instruction loads the stored value for ScoreX from the scratch space into Player1, adds 1 to it, and then stores the result back into ScoreX for the transaction sender.

Every time there is a winner the smart contract will be called and increase the score of X or O

The contract will be able to keep track of the scores for each player using the ScoreX and ScoreO local state variables.

```python
scorePlayer1 = Seq(   [
        Player1.store(App.localGet(Txn.sender(), Bytes('ScoreX'))),
        App.localPut(Txn.sender(), Bytes('ScoreX') , Player1.load() + Int(1)),
        Return(Int(1))

    ])

    scorePlayer2 = Seq(   [
        Player2.store(App.localGet(Txn.sender(), Bytes('ScoreO'))),
        App.localPut(Txn.sender(), Bytes('ScoreO'), Player2.load() + Int(1)),
        Return(Int(1))

    ])

```

App.localPut(Txn.sender(), Bytes('ScoreX') , Player1.load() + Int(0)): This instruction loads the stored value for ScoreX from the scratch space into Player1, adds 0 to it (i.e., does not change it), and then stores the result back into ScoreX for the transaction sender. This is for everytime there is no winner while playing.

```python
noScorePlayer1 = Seq(   [
        Player1.store(App.localGet(Txn.sender(), Bytes('ScoreX'))),
        App.localPut(Txn.sender(), Bytes('ScoreX') ,  Player1.load() + Int(0)),
        Return(Int(1))

    ])

```

handle_noop provides a way for the contract to handle different types of transactions and execute the appropriate sequence of instructions based on the arguments of the transaction. This can be useful for implementing different actions or game mechanics in the contract.

```python
 handle_noop = Seq(
        Assert(Global.group_size() == Int(1)),
        Cond(
            [Txn.application_args[0] == Bytes("scorePlayer1"), scorePlayer1],
            [Txn.application_args[0] == Bytes("noScorePlayer1"), noScorePlayer1],
            [Txn.application_args[0] == Bytes("scorePlayer2"), scorePlayer2],
            [Txn.application_args[0] == Bytes("noScorePlayer2"), noScorePlayer2],
        )
    )
```
