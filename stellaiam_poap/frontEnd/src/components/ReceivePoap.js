import React,{useEffect,useState} from "react";
import { useParams } from "react-router-dom";
import { Toaster ,toast } from 'react-hot-toast';

import { Table,Button,Checkbox ,Icon,Form, TextArea, Message,Item,List,Image,Comment,Header,Modal,Segment,Dimmer,Loader } from 'semantic-ui-react';

import Menu from "./Menu";
import Footer from "./Footer";
import { time_ago } from "./JyUtils";


const ReceivePoap = ()=>{
    require('dotenv').config;
    let { id } = useParams(); 

    const [poap, setPoap] = useState(null);
    const [secret, setSecret] = useState("");
    const [address, setAddress] = useState("");
    
    const [isProcess, setIsProcess] = useState(false);

    useEffect(()=>{

        const requestOptions = {
            method: 'GET',
            headers: { 
                "Access-Control-Allow-Origin": "http://127.0.0.1:8000/*",
                'Accept': 'application/json, text/plain',
                'Content-Type': 'application/json;charset=UTF-8',
            },
            mode:'cors'
        };

        // pass query params ref) https://stackoverflow.com/a/37230594
        fetch(`${process.env.REACT_APP_WEBSITE}api/get_poap/${id}`,requestOptions)
        .then((response)=>{
            console.log("response obj : ");
            console.dir(response);

            if(response.ok){

                
                return response.json();
            }else{
                if(response.status == 404 ){
                    instantMsg("Not found","normal");
                }else{
                    instantMsg("Failed to bring contents","warning");
                    throw Error("Failed communication with server for getting list of contents");
                }
            }
        }).then((data)=>{

            console.log("data.data",data.data)
            console.log("created : ",time_ago(data.data.created))


            setPoap(data.data)
            
        });


    },[]);

    const onChangeSecret = (event)=>{
        const value = event.target.value;
        setSecret(value);
    };

    const onChangeAddress = (event)=>{
        const value = event.target.value;
        setAddress(value);
    };

    const cleanStates = ()=>{

        setSecret("");
        setAddress("");
        
    };

    const onClickOkBtn = ()=>{
        console.log("onClickOkBtn called");

        setIsProcess(true);

        if(secret && address){

            if(isEthereumAddress(address)){
                const data = new FormData();

                data.append("poapId",id);
                data.append("secret",secret);
                data.append("address",address);
                
                const requestOptions = {
                    method: 'POST',
                    headers: { 
                        'Accept': 'application/json, text/plain'
                    },
                    body: data,
                    mode:'cors'
                };
    
                fetch(`${process.env.REACT_APP_WEBSITE}api/receive_poap/`,requestOptions)
                .then((response)=>{
                    console.log("response obj : ");
                    console.dir(response);
    
                    if(response.ok){
                        return response.json();
                    }else{
                        setIsProcess(false);
                        instantMsg("서버와의 통신에 문제가 있습니다","warning");
                    
                        throw Error("Failed communication with server for saving content");
                    }
                }).then((data)=>{
    
                    console.log("data",data);
    
                    console.log("Success saved content in server");

                    if(data.status == "success"){
                        instantMsg(data.msg,"normal");
                    }else{
                        instantMsg(data.msg,"warning");
                    }
    
                    setIsProcess(false);
                    cleanStates();
                    
                });

            }else{
                setIsProcess(false);
                instantMsg("지갑주소가 올바르지 않습니다","warning");
            }

        }else{
            setIsProcess(false);
            instantMsg("모든 항목을 작성하셔야 합니다","warning");
        }
    };

    const onClickCancelBtn = ()=>{
        console.log("onClickCancelBtn  called"); 

        cleanStates();
    };

    const onClickOpensea = ()=>{
        console.log("onClickOpensea called");
        console.log(process.env.REACT_APP_OPENSEA_URL);
        console.log(process.env.REACT_APP_STELLAIAM_POAP_CONTRACT_ADDRESS);

        window.open(`${process.env.REACT_APP_OPENSEA_URL}${process.env.REACT_APP_STELLAIAM_POAP_CONTRACT_ADDRESS}/${id}`, '_blank', 'noreferrer');
    };


    const instantMsg = (msg, type)=>{

        switch (type){
            case "normal":
                toast.success(msg,{duration: 8000});
            
                break;
            case "warning":
                toast.error(msg,{duration: 8000});
        }
    };

    const getCard = ()=>{
        return(
            <>

                <Table.Row>
                    <Table.Cell>
                    <div className="ui cards">
                        <div className="ui centered card">
                            <div className="image">
                                <img src={process.env.REACT_APP_WEBSITE+poap.image}/>
                            </div>
                            <div className="extra content">
                                <a>
                                <i className="clock icon"></i>
                                발행일 : {time_ago(poap.created)}
                                </a>
                                <br/>
                                <a>
                                <i className="user icon"></i>
                                발행자 : {poap.email}
                                </a>
                            </div>
                        </div>
                    </div>
                    </Table.Cell>
                    <Table.Cell id="poap_data_cell">
                        <h2>제목 : {poap.title}</h2>
                        <h4>내용 : {poap.description}</h4>
                        <br/>
                        <Button size='big' className="centered" color='yellow' onClick={onClickOpensea}>Opensea에서 확인하기</Button>
                    </Table.Cell>
                    
                </Table.Row>
            </>
        );
    };



    return(
        <>

            <Segment>
                <Dimmer active={isProcess}>
                    <Loader size='huge'>Processing</Loader>
                </Dimmer>


            <Menu updateProvider={()=>{}} updateCurrentAccount={()=>{}} updateChainId={()=>{}}/>

            

            <div id="body_component" className="ui centered one column grid">

                
                <div className="row">
                    <div className="column">


                    <Toaster/>

                    <Form>
                    <Table celled>
                        <Table.Header>
                            <Table.Row>
                                <Table.HeaderCell colSpan="2">
                                <h1>POAP 받기</h1>
                                </Table.HeaderCell>
                                
                            </Table.Row>
                            {poap && getCard()}
                        </Table.Header>

                        <Table.Body>
                            <Table.Row>
                                    <Table.Cell colSpan="2">
                                    
                                    <Form.Field>
                                        <input 
                                            placeholder='인증코드...'
                                            value={secret} 
                                            onChange={onChangeSecret}    
                                        />
                                    </Form.Field>
                                    
                                                                        
                                    </Table.Cell>   
                            </Table.Row>


                            <Table.Row>
                                    <Table.Cell colSpan="2">
                                    
                                    <Form.Field>
                                        <input 
                                            placeholder='지갑주소...'
                                            value={address} 
                                            onChange={onChangeAddress}    
                                        />
                                    </Form.Field>
                                    
                                                                        
                                    </Table.Cell>   
                            </Table.Row>
                    
                            <Table.Row>
                                <Table.Cell colSpan="2">
                                    <Button primary onClick={onClickOkBtn}>확인</Button>
                                    <Button secondary onClick={onClickCancelBtn}>취소</Button>
                                </Table.Cell>        
                            </Table.Row>
                            
                            
                        </Table.Body>
            
                        <Table.Footer>
                        <Table.Row>
                            <Table.HeaderCell colSpan="2"></Table.HeaderCell>

                        </Table.Row>
                        </Table.Footer>
                    </Table>
                    </Form>
                    </div>
                </div>
            </div>

            <Footer />
            </Segment>

        </>
    );
};

function isEthereumAddress(address){
    const { ethers, BigNumber } = require("ethers");

    return ethers.utils.isAddress(address);
}



export {ReceivePoap}