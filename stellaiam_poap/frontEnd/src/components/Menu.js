import Web3 from "web3";

import React, { useState, useEffect } from "react";
import { Image } from "semantic-ui-react";
import { Toaster ,toast } from 'react-hot-toast';

const Menu = (props)=>{
    const [provider,setProvider] = useState(null);
    const [chainId, setChainId] = useState(null);
    const [currentAccount,setCurrentAccount] = useState(null);

    const [isConnecting, setIsConnecting] = useState(false);

    

    const NETWORKS = {
        1: "Ethereum Main Network",
        3: "Ropsten Test Network",
        4: "Rinkeby Test Network",
        5: "Goerli Test Network",
        42: "Kovan Test Network",
        137: "Polygon Main Network",
        80001: "Mumbai Test Network"
    };




    // as soon as started, we get provider and save
    useEffect(() => {
        let provider;
        if (window.ethereum) {
            // user has metamask

            console.log("window.ethereum");
            // provider = window.ethereum;

            if(window.ethereum.providers){

                provider = window.ethereum.providers.find((provider) => provider.isMetaMask);
            }

            provider = window.ethereum;
        } else if (window.web3) {
            // user has different wallet

            console.log("window.web3");
            // provider = window.web3.currentProvider;

            provder = null;
        } else {
            // user doesn't have 

            console.warn("No Ethereum browser detected! Check out MetaMask");

            provider = null;
        }
        console.log("provider in detectProvider : ", provider);

        setProvider(provider);
        
    }, []);


    useEffect(() => {
        // update current account in main component
        props.updateProvider(provider);
    },[provider]);

    // when user click connect button, this func will be called
    const onLoginHandler = async () => {
        setIsConnecting(true);

        try{
            await provider.request({method: "eth_requestAccounts",});
        }catch(error){
            console.log("error :", error);
        }
        setIsConnecting(false);
        
        const web3 = new Web3(provider);
        const accounts = await web3.eth.getAccounts();
        const chainId = await web3.eth.getChainId();

        console.log("accounts.length :",accounts.length);
        console.log("chainId :",chainId);

        if (accounts.length === 0) {
            console.log("Please connect to MetaMask!");
        } 
        else if (accounts[0] !== currentAccount) {
            setChainId(chainId);
            setCurrentAccount(accounts[0]);
        }
    };

    // handle account changed , chain changed
    // and also remove handlers
    useEffect(() => {
        // update current account in main component
        props.updateCurrentAccount(currentAccount);


        const handleAccountsChanged = async (accounts) => {
            console.log("account changed");

            web3 = new Web3(provider);

            const web3Accounts = await web3.eth.getAccounts();
            if (accounts.length === 0) {
                onLogout();
            } else if (accounts[0] !== currentAccount) {
                setCurrentAccount(accounts[0]);
            }
        };

        const handleChainChanged = async (chainId) => {
            console.log("parseInt(chainId, 16) : ", parseInt(chainId, 16));
            
            const chainIdDec = parseInt(chainId, 16).toString();

            // this is redundance 
            // const web3ChainId = await web3.eth.getChainId();
           

            if(chainIdDec == 80001){
                // mumbai network supported

                instantMsg(NETWORKS[chainIdDec.toString()]+" 네트워크로 바뀌었습니다", "normal");
            }else{
                instantMsg("지원되지 않는 네트워크로 전환 되었습니다", "warning");
            }
            setChainId(chainIdDec);
        };

        if (currentAccount) {
            // attaching listener for metamask events
            console.log('metamask event listeners attached');
            provider.on("accountsChanged", handleAccountsChanged);
            provider.on("chainChanged", handleChainChanged);
        }

        // this func will be execute as cleaning up process whenever this component is disappeared
        return () => {
            if (currentAccount) {
                provider.removeListener("accountsChanged", handleAccountsChanged);
                provider.removeListener("chainChanged", handleChainChanged);
            }
        };
    }, [currentAccount]);


    useEffect(()=>{
        props.updateChainId(chainId)
    },[chainId]);

    const onLogout = () => {
        instantMsg("지갑연결이 끊어졌습니다", "warning")
        setChainId(null);
        setCurrentAccount(null);
    };


    const onClickConnectWallet = ()=>{
        console.log("onClickConnectWallet called");

        onLoginHandler();
    };


    const GoInstallMetamaskPage = ()=>{
        console.log("GoInstallMetamaskPage is called");
            
        window.open('https://metamask.io/download', '_blank', 'noreferrer');
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

    const getWalletBtn = (provider)=>{
        // console.log("getWalletBtn called");
        // console.log("provider : ",provider);
        console.log("window.location.pathname : ",window.location.pathname);

        const path = window.location.pathname.split("/");

        // when user receive they don't need to connect wallet
        if(path[1] == "" || path[1] == "receive_poap" || path[1] == "create_poap"){
            return(<></>);
        }

        if(provider){

            if(currentAccount){
                return(<>{smartTrim(currentAccount,8)}</>);
            }else{
                return(
                    <>

                    <button className="ui primary button" onClick={onClickConnectWallet}>
                    {!isConnecting && "지갑연결"}
                    {isConnecting && "지갑연결중..."}
                    </button>

                    </>
                );
            }

        }else{
            return(
                <>

                    <button className="ui primary button" onClick={GoInstallMetamaskPage}>
                    Metamask 페이지로 이동
                    </button>

                </>
            );
        }

        return (<></>);
    };

    
    return(

        <>
            
            <Toaster/>
            
            <div id="Menu" className="ui top fixed menu">
                <div className="item">
                    <Image size='tiny' src="/static/for_react/images/logo_color.png" />
                </div>
                <a className="item" href="/"><h4>Home</h4></a>
                <a className="item" href='/create_poap'><h4>POAP 만들기</h4></a>
                
                
                <div className="right menu">
                    <a className="ui item">
                    <h4>{getWalletBtn(provider)}</h4>
                    </a>
                </div>
            </div>
           

        </>

    );
};

export default Menu;




// ellipsis string ref) https://stackoverflow.com/a/831583
function smartTrim(string, maxLength) {
    if (!string) return string;
    if (maxLength < 1) return string;
    if (string.length <= maxLength) return string;
    if (maxLength == 1) return string.substring(0,1) + '...';

    var midpoint = Math.ceil(string.length / 2);
    var toremove = string.length - maxLength;
    var lstrip = Math.ceil(toremove/2);
    var rstrip = toremove - lstrip;
    return string.substring(0, midpoint-lstrip) + '...' 
    + string.substring(midpoint+rstrip);
}
