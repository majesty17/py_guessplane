<?php
$sql="select sum(d0),sum(d1),sum(d2),sum(d3),sum(d4),sum(d5),sum(d6),sum(d7),sum(d8),sum(d9),sum(d10),sum(d11),sum(d12),sum(d13),sum(d14),sum(d15),sum(d16),sum(d17),sum(d18),sum(d19),sum(d20),sum(d21),sum(d22),sum(d23),sum(d24),sum(d25),sum(d26),sum(d27),sum(d28),sum(d29),sum(d30),sum(d31),sum(d32),sum(d33),sum(d34),sum(d35),sum(d36),sum(d37),sum(d38),sum(d39),sum(d40),sum(d41),sum(d42),sum(d43),sum(d44),sum(d45),sum(d46),sum(d47),sum(d48),sum(d49),sum(d50),sum(d51),sum(d52),sum(d53),sum(d54),sum(d55),sum(d56),sum(d57),sum(d58),sum(d59),sum(d60),sum(d61),sum(d62),sum(d63),sum(d64),sum(d65),sum(d66),sum(d67),sum(d68),sum(d69),sum(d70),sum(d71),sum(d72),sum(d73),sum(d74),sum(d75),sum(d76),sum(d77),sum(d78),sum(d79),sum(d80),sum(d81),sum(d82),sum(d83),sum(d84),sum(d85),sum(d86),sum(d87),sum(d88),sum(d89),sum(d90),sum(d91),sum(d92),sum(d93),sum(d94),sum(d95),sum(d96),sum(d97),sum(d98),sum(d99),count(*) from test.data where 1=1 ";

$v0=$_GET["v0"];
$v1=$_GET["v1"];
$head=$_GET["h"];


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
#处理head等值
if($head!=""){
    $arr_h=split(",",$head);
    $str=implode(",",$arr_h);
    foreach($arr_h as $ah) {
        $sql=sprintf("%s and (h0=%s or h1=%s or h2=%s or h3=%s ) ",$sql,$ah,$ah,$ah,$ah);
    }
        # print $ah;
}else $arr_h=array();




if(isset($_GET['debug']))
    print_r($sql."<br>");


$con=mysql_connect('localhost','test_ro','1234');
if (!$con)
{
die('Could not connect: ' . mysql_error());
}
$result=mysql_db_query("test", $sql, $con);
$array=array();
for($i=0;$i<100;$i++) $array[$i]=0;
#取数&统计head出现次数
$row=mysql_fetch_row($result);



#标记有过的
foreach($bigarr as $aitem){
    $ind=(int)(str_replace("d","",$aitem));
    $row[$ind]=-1;

}

$middle=($row[100])/2;

$index=0;
$min=210000000;

if(isset($_GET['debug']))
    print_r("middle is ".$middle);


for($i=0;$i<100;$i++){
    if($row[$i]<1)continue;
    $dis=abs($middle-$row[$i]);
    if($dis<$min){
        $min=$dis;
        $index=$i;
    }
}

#print_r("max index is ".$index);
print_r("".(int)($index/10)."".chr($index%10+ord('a')));



mysql_close($con);
?>
