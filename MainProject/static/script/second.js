var currentStringId="refresult0";
const refaudio = new Audio();
const testaudio = new Audio();
var durdifference;
refaudio.src="";
testaudio.src="";
var duration="";
var reflinkdur="0";
var testlinkdur="0";
function stTolist(strg){
   duration="";
   var list=strg.replace(/'/g, '');
   list = list.replace(/\[/g, '');
   list = list.replace(/\]/g, '');
   list=list.split(",");
   var seqdata="", note="";
   for(i=0;i<list.length -1 ;i=i+3){
        note=list[i]+list[i+1];
        note=note.replace(/ /g, '');
        if(note=="--"){
            note="-";
        }
    seqdata=seqdata+" "+note;
    duration=duration+" "+list[i+2];
   
   }
   seqdata=seqdata.split(" ");
   seqdata=seqdata.filter(item => item !== null && item.trim() !== "");
   return seqdata;
}


function resultPlay(reff,testt){
    var refsource=document.getElementsByName("refsource")[0].innerText;
    var testsource=document.getElementsByName("testsource")[0].innerText;
    refaudio.src=refsource;
    testaudio.src=testsource;
    var ref=reff;
    var tes=testt;
    var reftimes=document.getElementById("reftimes").innerText;
    var testtimes=document.getElementById("testtimes").innerText;
    document.getElementById("reftimes").innerText="";
    document.getElementById("testtimes").innerText="";
    reftimes=reftimes.replace(/\[/g, '');
    reftimes=reftimes.replace(/\]/g, '');
    testtimes=testtimes.replace(/\]/g, '');
    testtimes=testtimes.replace(/\[/g, '');
    reftimes=reftimes.split(",");
    testtimes=testtimes.split(",");
    reftimes=reftimes.filter(item => item !== null && item.trim() !== "");
    testtimes=testtimes.filter(item => item !== null && item.trim() !== "");
    ref=stTolist(ref);

    var refduration=duration.split(" ");
    refduration=refduration.filter(item => item !== null && item.trim() !== "");
    var refplaytimes=duration.split(" ");
    refplaytimes=refplaytimes.filter(item => item !== null && item.trim() !== "");
    var rt=0;
    for(i=0;i<refduration.length;i++){
        if(refduration[i]=="-" && i==0){
            refduration[i]=0;
        }
        else if(refduration[i]=="-"){
            refduration[i]=refduration[i-1];
        }
        else{
            refduration[i]=parseFloat( reftimes[rt]);
            rt++;
        }
       }

    tes=stTolist(tes);
    

    var testduration=duration.split(" ");
    testduration=testduration.filter(item => item !== null && item.trim() !== "");
    var testplaytimes=duration.split(" ");
    testplaytimes=testplaytimes.filter(item => item !== null && item.trim() !== "");
    
    tt=0;
    for(i=0;i<testduration.length;i++){
        if(testduration[i]=="-" && i==0){
            testduration[i]=0;
        }
        else if(testduration[i]=="-"){
            testduration[i]=testduration[i-1];
        }
        else{
            testduration[i]=parseFloat( testtimes[tt]);
            tt++;
        }
       }
      
    var k=0;
    var flagerr=0;// note have no error
    var flagnoerr=0;// note have no error
    reflinkdur="0";
    testlinkdur="0";
    var reffnew="<table id='resultTable'><tr><td> <font color='#2a1444' size='6px'><pre style='tab-size:2;'>Reference Note Sequence  </pre> </font></td><td><label id='refresult"+k+"'>";
    var testtnew="<tr><td> <td> </tr><tr><td> <td> </tr><tr><td><font color='#2a1444' size='6px'><pre style='tab-size:2;' >Test Note Sequence  </pre></font></td><td><label id='testresult"+k+"'>";
    //***********for link do not consider the label with k=0*******
    var eflg=0;  // reference value is -
    var etflg=0;// test value is -
    for (i=0;i<ref.length;i++){
        if(ref[i]==tes[i]){
            if(flagerr==1 && flagnoerr==0 && i!=0){
                if(eflg==0){
                    reflinkdur=reflinkdur+" "+refduration[i];
                }
                if(etflg==0){
                    testlinkdur=testlinkdur+" "+testduration[i];
                }
                k=k+1;
                reflinkdur=reflinkdur+" "+refduration[i];
                testlinkdur=testlinkdur+" "+testduration[i];
                reffnew=reffnew+"</td><td></label><label id='refresult"+k+"'>";
                testtnew=testtnew+"</td><td></label><label id='testresult"+k+"'>";
                flagerr=0;
                flagnoerr=1;
            }
           
            durdifference=(((parseFloat(testplaytimes[i])) - (parseFloat(refplaytimes[i]))) ** 2);
            if(durdifference > 0.25 ){
                reffnew=reffnew+"<font color='#3f5c1e' size='5px'>"+" "+ref[i]+"</font>";
            testtnew=testtnew+"<font color='#3f5c1e' size='5px'>"+" "+tes[i]+"</font>";
            }
            else{
                reffnew=reffnew+"<font color='#127a38' size='5px'>"+" "+ref[i]+"</font>";
                testtnew=testtnew+"<font color='#127a38' size='5px'>"+" "+tes[i]+"</font>";
            }
           
            flagerr=0;
            flagnoerr=1;
            eflg=0;  // reference value is -
            etflg=0;
        }
        else{
    
            if(flagerr==0 && flagnoerr==1 && i!=0){
                k=k+1;
                if(refduration[i]!=refduration[i-1]){
                    eflg=1;  // reference value is -
                reflinkdur=reflinkdur+" "+refduration[i];
            }
                if(testduration[i]!=testduration[i-1]){
                etflg=1;// test value is -
                testlinkdur=testlinkdur+" "+testduration[i];
            }
                reffnew=reffnew+"</td><td></label><label id='refresult"+k+"'>";
                testtnew=testtnew+"</td><td></label><label id='testresult"+k+"'>";
                flagerr=1;
                flagnoerr=0;
            }
            if(flagerr==1 && flagnoerr==0 && i!=0){
                if(refduration[i]!=refduration[i-1] && eflg==0){
                    eflg=1;  // reference value is -
                reflinkdur=reflinkdur+" "+refduration[i];
            }
                if(testduration[i]!=testduration[i-1] && etflg==0){
                etflg=1;// test value is -
                testlinkdur=testlinkdur+" "+testduration[i];
            }}
            if(i==0){
                eflg=1; 
                etflg=1;  
            }
            if(ref[i]=='-'){
                reffnew=reffnew+"<font color='blue' size='5px'>"+" "+"  "+"</font>";
            }
            else{
                reffnew=reffnew+"<font color='blue' size='5px'>"+" "+ref[i]+"</font>";
            }
            if(tes[i]=='-'){
                testtnew=testtnew+"<font color='#f42c2b' size='5px'>"+" "+"  "+"</font>";
            }
            else{
                testtnew=testtnew+"<font color='#f42c2b' size='5px'>"+" "+tes[i]+"</font>";
            }
           
            flagerr=1;
            flagnoerr=0;
        }
    }
    reffnew="<b>"+reffnew+"</b></label></td></tr>";
    testtnew= "<b>"+testtnew+"</b></label></td></tr><tr> <td>  </td></tr></table>";
    reflinkdur=reflinkdur.split(" ");
    reflinkdur=reflinkdur.filter(item => item !== null && item.trim() !== "");
    testlinkdur=testlinkdur.split(" ");
    testlinkdur=testlinkdur.filter(item => item !== null && item.trim() !== "");    
    
    document.getElementById('newrf').innerHTML=" ";//reffnew;
    document.getElementById('newts').innerHTML=reffnew+testtnew;
    //+" "+k+" "+testlinkdur.length
    //link ref string with ref audio
    for(i=0;i<reflinkdur.length;i++){
       id1="refresult"+i;
       document.getElementById(id1).addEventListener('click', createEventListenerRef(i));
       }
//link test string with test audio
    for(i=0;i<testlinkdur.length;i++){
        id="testresult"+i;  
       document.getElementById(id).addEventListener('click',createEventListenerTest(i));
    }
    }

    function createEventListenerRef(t) {
        return async function() {
            document.getElementById(currentStringId).style.backgroundColor="white";
            currentStringId="refresult"+t;
            document.getElementById(currentStringId).style.backgroundColor="yellow";
            document.getElementById("refalignplay").innerHTML="Reference Audio <button id='refplay123'></button><button id='refstop123' style='display: none;'></button><br>";
            document.getElementById('refplay123').addEventListener('click',async function() {
                refaudio.currentTime=reflinkdur[t];
                refaudio.play();
                if(t!=(reflinkdur.length-1)){
                    setTimeout(function(){
                        refaudio.pause();
                        document.getElementById('refstop123').style.display = 'none';
                        document.getElementById('refplay123').style.display = 'inline';
                    },1000*(reflinkdur[t+1]-reflinkdur[t]));
                
                    
                }
                document.getElementById('refplay123').style.display = 'none';
                document.getElementById('refstop123').style.display = 'inline';
            });

            document.getElementById('refstop123').addEventListener('click',async function() {
                refaudio.pause();
                refaudio.currentTime = 0; 
                document.getElementById('refstop123').style.display = 'none';
                document.getElementById('refplay123').style.display = 'inline';
            });

        };
    }
    function createEventListenerTest(t) {
        
        return async function() {
            document.getElementById(currentStringId).style.background="white";
            currentStringId="testresult"+t;
            document.getElementById(currentStringId).style.background="yellow";
            document.getElementById("testalignplay").innerHTML="Test Audio <button id='testplay123'></button><button id='teststop123' style='display: none;'></button><br>";
            document.getElementById('testplay123').addEventListener('click',async function() {
                testaudio.currentTime=testlinkdur[t];
                testaudio.play();
                if(t!=(testlinkdur.length-1)){

                    setTimeout(function(){
                        testaudio.pause();
                        
                        document.getElementById('teststop123').style.display = 'none';
                        document.getElementById('testplay123').style.display = 'inline';
                    },1000*(testlinkdur[t+1]-testlinkdur[t]));
                   
                }
                document.getElementById('testplay123').style.display = 'none';
                document.getElementById('teststop123').style.display = 'inline';
            });
            document.getElementById('teststop123').addEventListener('click',async function() {
                testaudio.pause();
                testaudio.currentTime = 0; 
                document.getElementById('teststop123').style.display = 'none';
                document.getElementById('testplay123').style.display = 'inline';
            });

        };
    }

    function shownoteTimeseq(){
        document.getElementById('showNoteTime').style.display='inline';
        document.getElementById('btnShowNotime').style.display='none';
        document.getElementById('btnHideNotime').style.display='inline';
    }
    function hidenoteTimeseq(){
        document.getElementById('showNoteTime').style.display='none';
        document.getElementById('btnShowNotime').style.display='inline';
        document.getElementById('btnHideNotime').style.display='none';
    }
    function showAlignnoteTimeseq(){
        document.getElementById('showAlignNoteTime').style.display='inline';
        document.getElementById('btnShowAlignNotime').style.display='none';
        document.getElementById('btnHideAlignNotime').style.display='inline';
    }
    function hideAlignnoteTimeseq(){
        document.getElementById('showAlignNoteTime').style.display='none';
        document.getElementById('btnShowAlignNotime').style.display='inline';
        document.getElementById('btnHideAlignNotime').style.display='none';
    }
    function showAlignnoteseq(){
        document.getElementById('showAlignNote').style.display='inline';
        document.getElementById('btnShowAlignNote').style.display='none';
        document.getElementById('btnHideAlignNote').style.display='inline';
    }
    function hideAlignnoteseq(){
        document.getElementById('showAlignNote').style.display='none';
        document.getElementById('btnShowAlignNote').style.display='inline';
        document.getElementById('btnHideAlignNote').style.display='none';
    }

//display hints of colors in alignment
function hintsOfColor(){
    // document.getElementById('myhints').style.backgroundColor= "#0b0314" ;
    var hintColor=" ";
    hintColor=hintColor+"<font size='4.5px'><b><label style='color:#45226c'>Colour Hints...<label></b><br><button style='background-color:#127a38;' class='colorbtn'></button><label style='color:#127a38'>Corrected Notes<label>";
    hintColor=hintColor+"<br><button style='background-color:#3f5c1e;' class='colorbtn'></button><label style='color:#3f5c1e;text-align: left;'>Corrected Notes with Wrong duration<label>";
    hintColor=hintColor+"<br><button style='background-color:blue;' class='colorbtn'></button><label style='color:blue;text-align: left;'>Missed Notes<label>";
    hintColor=hintColor+"<br><button style='background-color:#f42c2b;' class='colorbtn'></button><label style='color:#f42c2b;text-align: left;'>Wrong Notes<label></font>";
    return hintColor;
    }