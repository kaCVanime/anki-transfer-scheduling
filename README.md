# Anki TransferScheduling
transfer scheduling info from cards to cards in batch

# Usage
### 1. Choose Deck
1) choose the source deck containing the source cards
2) choose the target deck containing the target cards

### 2. Add more detail
in the first transfer group
1) choose the note type of source/target card. 
> _if you don't know what note type it is_  
> a) click the `Browser` button located at the top of Anki.  
> b) switch to card view by clicking a blue/green switch, make sure it shows "Cards".   
> c) find the source card you want to transfer from.  
> d) right-click the card, click `Info...`.  
> e) in the pop-up window, Check the `Note Type` field.  
2) choose a field from source/target card for comparing.
3) choose the card template of source/target card.

### 3. (optional) Click Add Group button if you have more transfer type 

### 4. (optional) Check "Transfer Revision History" if you also want the revision history of source card be transferred.
warning. the revision history of target card will be overridden.

### 5. Click Start button


# Example
Imaging there are two different English vocabulary Deck, and we want to transfer scheduling info from Deck A to Deck B.  
The decks are configured as:
1. Deck A
All notes in Deck A, their note type is being named `A-Note`, it contains two fields, `word` and `definition`.
`A-Note` has 2 card templates, one named `word->definition` and the other named `definition->word`.
2. Deck B
Deck B has 2 subdecks, called `Deck B::Reading` and `Deck B::Writing` respectively.  
All notes in subdeck `Deck B::Reading`, their note type is being named `Note-Reading`, and it contains two fields, `term` and `def`.
All notes in subdeck `Deck B::Writing`, their note type is being named `Note-Writing`, and it contains two fields, `term` and `def`.


# Note
1. If a source card is new(hasn't been studied before), it will be skipped.  
