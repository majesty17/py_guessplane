<?php
$sql="select h0,h1,h2,h3 from test.data where 1=1 ";

$v0=$_GET["v0"];
$v1=$_GET["v1"];
$head=$_GET["h"];

if(isset($_GET['debug'])){
    $debug=true;
}
else $debug=false;


#处理等值
if($v0!=""){
    $arr_v0=split(",",$v0);
    foreach($arr_v0 as $i){
        $sql=$sql." and ".$i."=0";
    }
}else $arr_v0=array();

if($v1!=""){
    $arr_v1=split(",",$v1);
    foreach($arr_v1 as $i){
        $sql=$sql." and ".$i."=1";
    }
}else $arr_v1=array();

#处理head not in
$bigarr=array_merge($arr_v0,$arr_v1);
if(count($bigarr)>0){
    #print_r(implode(",",$bigarr));
    $str=implode(",",$bigarr);
    $str=str_replace("d","",$str);
    $sql=sprintf("%s and h0 not in(%s) and h1 not in(%s) and h2 not in(%s) and h3 not in(%s) ",$sql,$str,$str,$str,$str);

}
#处理head等值，有bug！！！
/*
if($head!=""){
    $arr_h=split(",",$head);
    $str=implode(",",$arr_h);
    $sql=sprintf("%s and (h0 in(%s) or h1 in (%s) or h2 in (%s) or h3 in (%s))",$sql,$str,$str,$str,$str);
}else $arr_h=array();*/

#新的处理head等值
if($head!=""){
    $arr_h=split(",",$head);
    foreach($arr_h as $ah) {
        $sql=sprintf("%s and (h0=%s or h1=%s or h2=%s or h3=%s ) ",$sql,$ah,$ah,$ah,$ah);
    }

}else $arr_h=array();


#这一步sql就ok了


if($debug)
    print_r("sql is [".$sql."]<br>");

$con=mysql_connect('localhost','test_ro','1234');
if (!$con)
{
die('Could not connect: ' . mysql_error());
}
$result=mysql_db_query("test", $sql, $con);
$array=array();
for($i=0;$i<100;$i++) $array[$i]=0;
#取数&统计head出现次数
while ($row=mysql_fetch_row($result)){
    $array[$row[0]]++;
    $array[$row[1]]++;
    $array[$row[2]]++;
    $array[$row[3]]++;
}


$leftct=mysql_affected_rows();
if($debug)
    print_r("total case count is [".$leftct."]<br>");


#置已有head为0
foreach($arr_h as $ah){
    $array[$ah]=0;
}


#找到头部出现最多的位置&打印矩阵
$max=$array[0];
$index=0;
for($i=0;$i<100;$i++){
#    if($debug){
#        print_r($array[$i].",\t");
#        if(($i+1)%10==0) print_r("<br>");
#    }
    if($array[$i]>=$max){
        $max=$array[$i];
        $index=$i;
    }

}
#print 
if($debug){
    print_r("<table border=1><tr>");
    for($i=0;$i<100;$i++){
        $collevel=sprintf("%02x",255-(int)$array[$i]/$leftct*255);
        print_r("<td bgcolor='#ff".$collevel.$collevel."'>".$array[$i].sprintf("(%.2f%%)",$array[$i]*100.0/$leftct)."</td>");
        if(($i+1)%10==0) print_r("</tr><tr>");
    }
    print_r("</tr></table>");

}




#1,末尾优化
#末尾如果都是1，则使用最接近折半的一个
if($max==1 and $leftct>5){
    $index2=-1;
    $min=21000000;
    $sql2=str_replace("h0,h1,h2,h3","sum(d0),sum(d1),sum(d2),sum(d3),sum(d4),sum(d5),sum(d6),sum(d7),sum(d8),sum(d9),sum(d10),sum(d11),sum(d12),sum(d13),sum(d14),sum(d15),sum(d16),sum(d17),sum(d18),sum(d19),sum(d20),sum(d21),sum(d22),sum(d23),sum(d24),sum(d25),sum(d26),sum(d27),sum(d28),sum(d29),sum(d30),sum(d31),sum(d32),sum(d33),sum(d34),sum(d35),sum(d36),sum(d37),sum(d38),sum(d39),sum(d40),sum(d41),sum(d42),sum(d43),sum(d44),sum(d45),sum(d46),sum(d47),sum(d48),sum(d49),sum(d50),sum(d51),sum(d52),sum(d53),sum(d54),sum(d55),sum(d56),sum(d57),sum(d58),sum(d59),sum(d60),sum(d61),sum(d62),sum(d63),sum(d64),sum(d65),sum(d66),sum(d67),sum(d68),sum(d69),sum(d70),sum(d71),sum(d72),sum(d73),sum(d74),sum(d75),sum(d76),sum(d77),sum(d78),sum(d79),sum(d80),sum(d81),sum(d82),sum(d83),sum(d84),sum(d85),sum(d86),sum(d87),sum(d88),sum(d89),sum(d90),sum(d91),sum(d92),sum(d93),sum(d94),sum(d95),sum(d96),sum(d97),sum(d98),sum(d99)",$sql);
    if($debug) print $sql2;
    $result=mysql_db_query("test", $sql2, $con);
    $row2=mysql_fetch_row($result);

#var_dump($array);
    for($i=0;$i<100;$i++){
        if($array[$i]==0) continue;
        $dis=abs($leftct/2-$row2[$i]);
        if($dis<$min){
            $min=$dis;
            $index2=$i;
        }
    }
    $index=$index2;
}






#2,如果中间出现多个相等的最大点,则取最接近二分的
$max_keys=array_keys($array,$max); #所有等于max的index
if($max>1 && count($max_keys)>=2) {    #等于1的\maxvalue小于2的，不走
    if($debug) var_dump(array_keys($array,$max));
    if($debug) print "<br>";

    $str_select ="";

    for($i=0;$i<count($max_keys);$i++){
        $str_select=sprintf("%s,sum(d%d)",$str_select,$max_keys[$i]);
    }
    $str_select=substr($str_select,1);
    #echo $str_select;
    $sql3=str_replace("h0,h1,h2,h3",$str_select,$sql);
    if($debug) print $sql3."<br>";
    $result3=mysql_db_query("test", $sql3, $con);
    $row3=mysql_fetch_row($result3);

    if($debug) var_dump($row3);

    #找到离中间值最近的
    $index3=0;
    $min=21000000;

    for($i=0;$i<count($row3);$i++){
        $dis=abs($leftct/2-$row3[$i]);
        if($dis<$min){
            $min=$dis;
            $index3=$i;
        }
    }
    $index=$max_keys[$index3];

}
















#输出下一步的决策
#print_r("max index is ".$index);
print_r("".(int)($index/10)."".chr($index%10+ord('a')));



mysql_close($con);
?>
