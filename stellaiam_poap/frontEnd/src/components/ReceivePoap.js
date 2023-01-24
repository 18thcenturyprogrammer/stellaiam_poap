import React,{useEffect,useState} from "react";
import { useParams } from "react-router-dom";
import { Toaster ,toast } from 'react-hot-toast';

import { Table,Button,Checkbox ,Icon,Form, TextArea, Message,Item,List,Image,Comment,Header,Modal,Segment,Dimmer,Loader } from 'semantic-ui-react';

import Menu from "./Menu";
import Footer from "./Footer";

const ReceivePoap = ()=>{
    let { id } = useParams(); 

    const [secret, setSecret] = useState("");
    const [address, setAddress] = useState("");

    const [isProcess, setIsProcess] = useState(false);

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


        if(secret && address){

            if(isEthereumAddress(address)){
                data.append("secret",secret);
                data.append("address",address);
                
                // const requestOptions = {
                //     method: 'POST',
                //     headers: { 
                //         'Accept': 'application/json, text/plain'
                //     },
                //     body: data,
                //     mode:'cors'
                // };
    
                // fetch("http://127.0.0.1:8000/api/create_single_direct_poap_claim/",requestOptions)
                // .then((response)=>{
                //     console.log("response obj : ");
                //     console.dir(response);
    
                //     if(response.ok){
                //         return response.json();
                //     }else{
                //         setIsProcess(false);
                //         instantMsg("서버와의 통신에 문제가 있습니다","warning");
                    
                //         throw Error("Failed communication with server for saving content");
                //     }
                // }).then((data)=>{
    
                //     console.log("data",data);
                    
                //     console.log(data.data.id);
    
                //     console.log("Success saved content in server");
    
                //     setIsProcess(false);
                //     setModalOpen(true)
                //     setClaimId(data.data.id);
                    
                // });

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


    const instantMsg = (msg, type)=>{

        switch (type){
            case "normal":
                toast.success(msg,{duration: 8000});
            
                break;
            case "warning":
                toast.error(msg,{duration: 8000});
        }
    };



    return(
        <>

            <Segment>
                <Dimmer active={isProcess}>
                    <Loader size='huge'>Processing</Loader>
                </Dimmer>


            <Menu updateProvider={()=>{}} updateCurrentAccount={()=>{}} updateChainId={()=>{}}/>

            

            <div id="body_component" className="ui centered one column grid">
                
                <div className="column row">
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