from pyteal import *

def approval_program():
    handle_creation = Seq([
        App.globalPut(Bytes("Count"), Int(0)),
        Return(Int(1))
    ])

    handle_creationX = Seq([
    App.localPut(Txn.sender(),Bytes('ScoreX'), Int(0)),  #uint64
    Return(Int(1))
    ])
    handle_creationO = Seq([
    App.localPut(Txn.sender(),Bytes('ScoreO'), Int(0)),  #uint64
    Return(Int(1))
    ])

    handle_optin = Return(Int(1))
    handle_closeout = Return(Int(0))
    handle_updateapp = Return(Int(0))
    handle_deleteapp = Return(Int(0))
    
    Player1 = ScratchVar(TealType.uint64)
    Player2 = ScratchVar(TealType.uint64)


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
    noScorePlayer1 = Seq(   [
        Player1.store(App.localGet(Txn.sender(), Bytes('ScoreX'))),
        App.localPut(Txn.sender(), Bytes('ScoreX') ,  Player1.load() + Int(0)),
        Return(Int(1))

    ])
    # player 2

    noScorePlayer2 = Seq(   [
        Player2.store(App.localGet(Txn.sender(), Bytes('ScoreO'))),
        App.localPut(Txn.sender(), Bytes('ScoreO'),  Player2.load() + Int(0)),
        Return(Int(1))

    ])
    handle_noop = Seq(
        Assert(Global.group_size() == Int(1)), 
        Cond(
            [Txn.application_args[0] == Bytes("scorePlayer1"), scorePlayer1], 
            [Txn.application_args[0] == Bytes("noScorePlayer1"), noScorePlayer1],
            [Txn.application_args[0] == Bytes("scorePlayer2"), scorePlayer2], 
            [Txn.application_args[0] == Bytes("noScorePlayer2"), noScorePlayer2],
        )
    )

    program = Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.application_id() == Int(0), handle_creationX],
        [Txn.application_id() == Int(0), handle_creationO],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_updateapp],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )

    return compileTeal(program, Mode.Application, version=5)

def clear_state_program():
    program = Return(Int(1))
    return compileTeal(program, Mode.Application, version=5)

appFile = open('approval.teal', 'w')
appFile.write(approval_program())
appFile.close()
 
clearFile = open('clear.teal','w')
clearFile.write(clear_state_program())
clearFile.close()
