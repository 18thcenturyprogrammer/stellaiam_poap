
import React, {useEffect, useState} from "react";

import { Toaster ,toast } from 'react-hot-toast';

import { Table,Button,Checkbox ,Icon,Form, TextArea, Message,Item,List,Image,Comment,Header,Modal,Segment,Dimmer,Loader } from 'semantic-ui-react';
import {
    MDBBtn,
    MDBModal,
    MDBModalDialog,
    MDBModalContent,
    MDBModalHeader,
    MDBModalTitle,
    MDBModalBody,
    MDBModalFooter,
  } from 'mdb-react-ui-kit';

import $ from 'jquery';

import Menu from "./Menu";
import Footer from "./Footer";

const contractAddress = process.env.REACT_APP_STELLAIAM_POAP_CONTRACT_ADDRESS;
console.log("########contract addres#############", contractAddress);

const SendPoapNonDirect = ()=>{
    require('dotenv').config;
    console.log(process.env);
    
    const [currentAccount, setCurrentAccount] = useState(null);
    const [provider, setProvider] = useState(null);
    const [chainId, setChainId] = useState(0);

    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [email, setEmail] = useState("");
    
    const [howMany, setHowMany] = useState(1);
    const [secret, setSecret] = useState("");

    const [image, setImage] = useState(null);
    const [hasAgreed, setHasAgreed] = useState(false);

    const [claimId, setClaimId] = useState(null);

    const [modalOpen, setModalOpen] = useState(false);
    const [isProcess, setIsProcess] = useState(false);

    const NETWORKS = {
        1: "Ethereum Main Network",
        3: "Ropsten Test Network",
        4: "Rinkeby Test Network",
        5: "Goerli Test Network",
        42: "Kovan Test Network",
        137: "Polygon Main Network",
        80001: "Mumbai Test Network"
    };

    useEffect(()=>{
        cleanStates()
    },[currentAccount]);

    useEffect(()=>{
        cleanStates()
    },[chainId]);


    const updateProvider = (pro)=>{
        setProvider(pro);

        console.log("provider is updated in main component");
        console.log("pro : ",pro);
    };

    const updateCurrentAccount = (acct)=>{
        setCurrentAccount(acct);

        console.log("acct is updated in main component");
        console.log("acct : ",acct);
    };


    const updateChainId = (id)=>{
        setChainId(id);

        console.log("id is updated in main component");
        console.log("id : ",id);
    };

    
    const onChangeEmail = (event)=>{
        const value = event.target.value;
        setEmail(value);
    };

    const onChangeTitle = (event)=>{
        const value = event.target.value;
        setTitle(value);
    };

    const onChangeDescription = (event)=>{
        const value = event.target.value;
        setDescription(value);
    };


    const onImageChange = (event) =>{
        console.log("onImageChange called");

        const file = event.target.files[0];

        console.log("============= file =================");
        console.dir(file);

        if(file){
            if (isFileImage(file)){
                // image file

                if(isRightSizeFile(file)){
                    // rigth size

                    setImage(file);
                }else{
                    instantMsg('??????????????? 10MB ?????? ????????? ?????????','warning');
                    event.target.value = null;
                    setImage(null);
                }
    
                
            }else{
                instantMsg('????????? ????????? ????????????','warning');
                event.target.value = null;
                setImage(null);
            }
        }else{
            event.target.value = null;
            setImage(null);
        }
    }


    const onChangeHowMany = (event)=>{
        console.log("onChangeHowMany called");

        const value = event.target.value;
        setHowMany(value);
    };

    const onChangeSecret = (event)=>{
        const value = event.target.value;
        setSecret(value);
    };



    const getChainIdAlert = ()=>{
        if(currentAccount && chainId != 80001){
            return(
                <>
                    <div className="right menu">
                        
                        <div class="ui negative message">
                            <i class="close icon"></i>
                            <div class="header">
                                Polygon ??????????????? ???????????? !!!
                            </div>
                            <p>???????????? ?????? ?????????????????? ????????? ????????? ???????????? ????????????</p>
                        </div>
                        
                    </div>
                </>
            );
        }else{
            return("");
        }
    };

    const onChangeTandC = (event, data)=>{
        console.log("onChangeTandC  called"); 
        console.dir(event);
        console.log("=======");
        console.dir(data);
        
        setHasAgreed(data.checked);
    };

    const cleanFileLabels = ()=>{
        $(".file").val('');
    };

    const cleanStates = ()=>{

        setTitle("");
        setDescription("");
        setEmail("");
        setHowMany(1);
        setImage(null);
        setHasAgreed(false);
        setClaimId(null);
        cleanFileLabels();
        setSecret("")

        setModalOpen(false);
        setIsProcess(false);
    };



    const onClickOkBtn = ()=>{
       console.log("onClickOkBtn  called"); 

       setIsProcess(true);

        // check provider, wallet before sending data to server
        if(provider && currentAccount){

            console.log("1");

            // check all fields is filled
            if(title && description && email && image && hasAgreed && howMany && secret){

                console.log("2");

                if(validateEmail(email)){
                    console.log("3");

                    if(isPositiveInt(howMany) && howMany > 1){
                        
                        const data = new FormData();
                    
                        data.append("title",title);
                        data.append("description",description);
                        data.append("email",email);
                        data.append("image", image);
                        data.append("howMany",howMany);
                        data.append("secret",secret);
                        
                        const requestOptions = {
                            method: 'POST',
                            headers: { 
                                'Accept': 'application/json, text/plain'
                            },
                            body: data,
                            mode:'cors'
                        };
            
                        fetch(`${process.env.REACT_APP_WEBSITE}api/create_non_direct_poap_claim/`,requestOptions)
                        .then((response)=>{
                            console.log("response obj : ");
                            console.dir(response);
            
                            if(response.ok){
                                return response.json();
                            }else{
                                setIsProcess(false);
                                instantMsg("???????????? ????????? ????????? ????????????","warning");
                            
                                throw Error("Failed communication with server for saving content");
                            }
                        }).then((data)=>{
            
                            console.log("data",data);
                            
                            console.log(data.data.id);

                            console.log("Success saved content in server");

                            setIsProcess(false);
                            setModalOpen(true)
                            setClaimId(data.data.id);
                            
                        });

                    }else{

                        // howMany is not positive number

                        setIsProcess(false);
                        setHowMany(0);
                        instantMsg("????????? ????????? ???????????????","warning");

                    }

                }else{
                    setIsProcess(false);
                    instantMsg("?????????????????? ???????????? ????????????", "warning");
                }

            }else{
                setIsProcess(false);
                instantMsg("?????? ????????? ???????????? ???????????? ??????????????? ?????????","warning");
            }

        }else{
            setIsProcess(false);
            instantMsg("????????? ???????????? ?????? ????????????","warning");
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

    const changeModalOpen = () => setModalOpen(!modalOpen);

    const onClickSendPoap = async ()=>{
        console.log("onClickSendPoap called");

        setModalOpen(false);
        setIsProcess(true);

        const { ethers, BigNumber } = require("ethers");

        const abi = process.env.REACT_APP_ABI;
        const contractAddress = process.env.REACT_APP_STELLAIAM_POAP_CONTRACT_ADDRESS;

        console.log("########contract addres#############", contractAddress);

        const provider = new ethers.providers.Web3Provider(window.ethereum, "any");
        const stellaiamPoapContract = new ethers.Contract(contractAddress,abi,provider);

        // Prompt user for account connections
        await provider.send("eth_requestAccounts", []);
        const signer = provider.getSigner();

        // const connectedWallet = signer.connect(provider);

        const gasData = await provider.getFeeData();

        // if i follow eip 1559, i can't override gasprice option
        // maxFeePerGas must be higher than maxPriorityFeePerGas
        // old stable values 50,40
        const mulMaxFeePerGas = gasData.maxFeePerGas.mul(BigNumber.from(5));
        const mulMaxPriorityFeePerGas = gasData.maxPriorityFeePerGas.mul(BigNumber.from(3));
               
        
        const decimals = 15;
        const input = process.env.REACT_APP_FEE*howMany*1000;

        console.log("input :",input);

        const amount = BigNumber.from(input).mul(BigNumber.from(10).pow(decimals));

        console.log("amount :",amount);

        console.log("Number(amount) :",Number(amount));

        // normal gasLimit is 21000 , but not worked ,so i changed it to this
        const options = {
            value: amount,
            gasLimit:ethers.utils.hexlify(1000000),
            maxFeePerGas:mulMaxFeePerGas,
            maxPriorityFeePerGas:mulMaxPriorityFeePerGas,
            nonce: await provider.getTransactionCount(currentAccount)
        };

        
        // send transaction with value
        // ref) https://vsupalov.com/ethers-call-payable-solidity-function/
        const result = await stellaiamPoapContract.connect(signer).paidByUser(claimId,howMany, options).then(async (result)=>{

            const txReceipt = await result.wait();

            console.log("txReceipt : ", txReceipt);
            console.dir(txReceipt);

            if(txReceipt.blockNumber){
                console.log("claim paid successfully");

                sendTxToServer(txReceipt.transactionHash)

                instantMsg("????????? ?????????????????????","normal");
                
                cleanStates();
                
            }else{
                instantMsg("???????????? ???????????? ????????? ??????????????????","warning");
            }

        }).catch((err)=>{
            console.log("error while doing transaction paidByUser");
            instantMsg("???????????? ???????????? ????????? ??????????????????","warning");
        });
        
        

        setIsProcess(false);


    };

    const sendTxToServer = (paidTxHash)=>{
        const data = new FormData();

        data.append("paidTxHash",paidTxHash);
       
        const requestOptions = {
            method: 'POST',
            headers: { 
                'Accept': 'application/json, text/plain'
            },
            body: data,
            mode:'cors'
        };

        fetch(`${process.env.REACT_APP_WEBSITE}api/public_paid_non_direct_poap_claim/`,requestOptions)
        .then((response)=>{
            console.log("response obj : ");
            console.dir(response);

            if(response.ok){
                return response.json();
            }else{
                instantMsg("???????????? ????????? ????????? ????????????","warning");
            
                throw Error("Failed communication with server for saving content");
            }
        }).then((data)=>{

            console.log("data",data);

            console.log("Success saved content in server");
            
        });
    };

    return (
        <>
            <MDBModal tabIndex='-1' show={modalOpen} setShow={setModalOpen}>
                <MDBModalDialog centered>
                <MDBModalContent>
                    <MDBModalHeader>
                    <MDBModalTitle>POAP ?????????</MDBModalTitle>
                    <MDBBtn className='btn-close' color='none' onClick={changeModalOpen}></MDBBtn>
                    </MDBModalHeader>
                    <MDBModalBody>
                    <h4>
                        POAP ??? {howMany}??? ???????????????
                    </h4>
                    <h4>
                        {parseFloat(process.env.REACT_APP_FEE*howMany)} Matic ????????? ????????? 
                    </h4>
                    <h4>???????????????????????? ?</h4>
                    </MDBModalBody>
                    <MDBModalFooter>
                    <MDBBtn color='secondary' onClick={changeModalOpen}>
                        ?????????
                    </MDBBtn>
                    <MDBBtn onClick={onClickSendPoap}>??? ?????????????????????</MDBBtn>
                    </MDBModalFooter>
                </MDBModalContent>
                </MDBModalDialog>
            </MDBModal>

            <Segment>
                <Dimmer active={isProcess}>
                    <Loader size='huge'>Processing</Loader>
                </Dimmer>


            <Menu updateProvider={updateProvider} updateCurrentAccount={updateCurrentAccount} updateChainId={updateChainId}/>

            

            <div id="body_component" className="ui centered one column grid">
                <div className="column row">
                    <div className="column">
                    {getChainIdAlert(chainId)}
                    </div>
                </div>


                <div className="column row">
                    <div className="column">


                    <Toaster/>

                    <Form>
                    <Table celled>
                        <Table.Header>
                            <Table.Row>
                                <Table.HeaderCell colSpan="2">
                                <h1>POAP ????????? ?????? ?????? ?????????</h1>
                                </Table.HeaderCell>
                                
                            </Table.Row>
                        </Table.Header>

                        <Table.Body>
                            <Table.Row>
                                    <Table.Cell colSpan="2">
                                    
                                    <Form.Field>
                                        <input 
                                            id='titleInput' 
                                            placeholder='???????????? ?????????...'
                                            value={email} 
                                            onChange={onChangeEmail}    
                                        />
                                    </Form.Field>
                                    
                                                                        
                                    </Table.Cell>   
                            </Table.Row>


                            <Table.Row>
                                    <Table.Cell colSpan="2">
                                    
                                    <Form.Field>
                                        <input 
                                            id='titleInput' 
                                            placeholder='??????...'
                                            value={title} 
                                            onChange={onChangeTitle}    
                                        />
                                    </Form.Field>
                                    
                                                                        
                                    </Table.Cell>   
                            </Table.Row>
                            
                            <Table.Row>
                                <Table.Cell colSpan="2">
                                
                                    <TextArea 
                                        placeholder='??????...' 
                                        style={{ minHeight: 100 }} 
                                        value={description} 
                                        onChange={onChangeDescription}
                                    />
                                
                                                                    
                                </Table.Cell>   
                            </Table.Row>
                            <Table.Row>
                                <Table.Cell colSpan="2">
                                POAP ????????? &#58; <input className="file" accept="image/*" id='image' type="file" onChange={onImageChange}/>
                                </Table.Cell>
                            </Table.Row>
                            <Table.Row>
                                <Table.Cell colSpan="2">
                                    
                                    <div class="ui right labeled input">
                                        <input value={howMany} type="number" step="1" pattern="\d+" min="2" onChange={onChangeHowMany} placeholder="??????..." />
                                        <div class="ui basic label">
                                            ???
                                        </div>
                                    </div>
                                    
                                </Table.Cell>
                                
                            </Table.Row>
                            <Table.Row>
                                <Table.Cell>

                                    <Form.Field>
                                        <input 
                                            id='titleInput' 
                                            placeholder='????????????'
                                            value={secret} 
                                            onChange={onChangeSecret}    
                                        />
                                    </Form.Field>
                                    
                                </Table.Cell>
                                <Table.Cell>

                                    <p>POAP??? ???????????? ???????????? ???????????? ?????? ?????????????????????</p>

                                </Table.Cell>
                            </Table.Row>
                            <Table.Row>
                                <Table.Cell colSpan='2'>
                                    <Form.Field>
                                        <Checkbox checked={hasAgreed} onChange ={(evt,data)=>{onChangeTandC(evt,data)}} label="Stellaiam ?????? ????????? ???????????????" />
                                    </Form.Field>
                                </Table.Cell>
                            </Table.Row>
                    
                            <Table.Row>
                                <Table.Cell colSpan="2">
                                    <Button primary onClick={onClickOkBtn}>??????</Button>
                                    <Button secondary onClick={onClickCancelBtn}>??????</Button>
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




// check file is image type or not
// ref) https://roufid.com/javascript-check-file-image/
function isFileImage(file) {
    const acceptedImageTypes = ['image/gif', 'image/jpeg', 'image/png'];

    return acceptedImageTypes.includes(file['type'])
}

function isXlsxCsv(file){
    console.log("isXlsxCsv called");
    console.dir(file);

    if(file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" || file.type == "text/csv"){
        // only accept xlsx , csv
        return true;
    }else{
        return false;
    }
}


function isRightSizeFile(file) {
                    
    // file size limit is 10 mb
    return file.size <= 10240000
}

// check email address is correct 
// ref) https://stackoverflow.com/a/9204568
function validateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}


function isEthereumAddress(address){
    const { ethers, BigNumber } = require("ethers");

    return ethers.utils.isAddress(address);
}


// convert array into csv string
// ref) https://stackoverflow.com/a/68146412
function arrayToCsv(data){
    return data.map(row =>
      row
      .map(String)  // convert every value to String
      .map(v => v.replaceAll('"', '""'))  // escape double colons
      .map(v => `"${v}"`)  // quote it
      .join(',')  // comma-separated
    ).join('\r\n');  // rows starting on new lines
}

// check positive integer or not
// ref) https://stackoverflow.com/questions/10834796/validate-that-a-string-is-a-positive-integer
function isPositiveInt(str) {
    var n = Math.floor(Number(str));
    return n !== Infinity && String(n) === str && n > 0;
}

export {SendPoapNonDirect, isFileImage, isXlsxCsv, isRightSizeFile, validateEmail, isEthereumAddress, arrayToCsv,isPositiveInt};