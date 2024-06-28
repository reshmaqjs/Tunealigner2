
def myDTW(r,t):
    seq1=r
    seq2=t
    csize=len(seq1)+1
    rsize=len(seq2)+1
    # variables to the calculation of value of cell
    left=0
    top=0
    diag=0
    match=1  #match score
    mismatch=-2  #mismatch score
    gap=-1  #gap penalty
    backmove=[]#list for backward movement from similarity matrix
    mat=[[0 for j in range(csize)]for i in range(rsize)]
    #set values at first column as 0 -1 -2 -3 ....
    for i in range(rsize):
        mat[i][0]=-i
    #set values at first raw as 0 -1 -2 -3 ....
    for i in range(csize):
        mat[0][i]=-i
    #find score matrix  
    for i in range(1,rsize):
        for j in range(1,csize):
            left=mat[i][j-1]+gap
            top=mat[i-1][j]+gap
            diag=mat[i-1][j-1]+mismatch
            if(seq1[j-1][0]==seq2[i-1][0] and seq1[j-1][1]==seq2[i-1][1]):
                diag=mat[i-1][j-1]+match
                
            mat[i][j]=max([left,top,diag])
    raw=rsize-1
    col=csize-1
    #back tracking
    while(1==1):
        if raw!=0 and col!=0:
            if mat[raw][col]==mat[raw-1][col-1]+match and seq1[col-1][0:2]==seq2[raw-1][0:2]: #'''and (not(col==1 and raw!=1) and not(col!=1 and raw==1))'''
                backmove.append("d")
                raw=raw-1
                col=col-1            
            elif mat[raw][col]==mat[raw][col-1]+gap: #'''and (not(col==1 and raw!=1))'''
                backmove.append("l")
                col=col-1
            elif  mat[raw][col]==mat[raw-1][col]+gap: # '''and (not(col!=1 and raw==1))'''
                backmove.append("u")
                raw=raw-1
            elif mat[raw][col]==mat[raw-1][col-1]+mismatch: # '''and (not(col==1 and raw!=1)) and (not(col!=1 and raw==1)) and raw!=0 and col!=0''':
                backmove.append("d")
                raw=raw-1
                col=col-1
        elif col!=0:
            if mat[raw][col]==mat[raw][col-1]+gap:
                backmove.append("l")
                col=col-1
        elif raw!=0:
            if mat[raw][col]==mat[raw-1][col]+gap:
                backmove.append("u")
                raw=raw-1
        else:
            break
        
    s1=[]
    s2=[]
    r=len(seq1)-1
    c=len(seq2)-1
    for i in backmove:
        if i=='d':
            s1.append(seq1[r])
            s2.append(seq2[c])
            r=r-1
            c=c-1
        elif i=='l':
            s1.append(seq1[r])
            s2.append(['-','-','-'])
            r=r-1
        elif i=='u':
            s1.append(['-','-','-'])
            s2.append(seq2[c])
            c=c-1
    s1=s1[::-1]
    s2=s2[::-1]
    score=0
    for i in range(len(s1)):
        if s1[i][0:2]==s2[i][0:2]:
            score=score+1
        elif s1[i][0]=='-' or s2[i][0]=='-':
            score=score
        else :
            score=score-1
    return mat,s1,s2,score

def Make_DiffList(inc,dec,seq):
    list_of_lists=[seq]
    temp1=seq
    temp2=seq
    for i in range(inc):
        print (i)
        temp1=[ [j[0],str(int(j[1])+1),j[2]] for j in temp1]
        list_of_lists.append(temp1)
    for i in range(dec):
        temp2=[ [j[0],str(int(j[1])-1),j[2]] for j in temp2]
        list_of_lists.append(temp2)
    return list_of_lists

def AlignBest(ref,test):
    print("Alignment working.....")
    refnew=[ [i[0][0],i[0][1],i[1]] for i in ref]
    testnew=[ [i[0][0],i[0][1],i[1]] for i in test]
    print(refnew)
    print(testnew)
    refOctaves=[i[1] for i in refnew]
    rmaxOctave=int(max(refOctaves))
    rminOctave=int(min(refOctaves))

    testOctaves=[i[1] for i in testnew]
    tmaxOctave=int(max(refOctaves))
    tminOctave=int(min(refOctaves))
    increments=rmaxOctave-tminOctave
    decrements=tmaxOctave-rminOctave
    print("rmaxOctave ",rmaxOctave,"  rminOctave ",rminOctave,"  tminOctave ",tminOctave,"  tmaxOctave ",tminOctave,"  increments ",increments,"  decrements ",decrements)
    ListOf_Test_Seq_List = Make_DiffList(increments,decrements,testnew)
    print("\nListOf_Test_Seq_List : ",ListOf_Test_Seq_List)
    Best_similaritymat, Best_align_s1, Best_align_s2, Best_score = myDTW( refnew, ListOf_Test_Seq_List[0])

    for k in range (len(ListOf_Test_Seq_List)):
        similaritymat,align_s1,align_s2,score=myDTW(refnew,ListOf_Test_Seq_List[k])
        print("score",score)
        print(align_s1," \n",align_s2)
        if (Best_score < score):
            print("y")
            Best_similaritymat,Best_align_s1,Best_align_s2,Best_score=similaritymat,align_s1,align_s2,score
            
    print("\nSimilarity matrix" ,Best_similaritymat)
    print ("\nAlignment of reference and test sequences\n",Best_align_s1)
    print (Best_align_s2)
    print ("\n Score \n",Best_score)
    AlinPercent=100*(Best_score/len(Best_align_s1))
    return Best_align_s1,Best_align_s2,AlinPercent