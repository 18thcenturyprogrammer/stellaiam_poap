import React, { Component, useEffect, useState } from "react";
import { Label, Image, Icon } from "semantic-ui-react";


const ConnectButton = (props)=>{
    const [isConnecting, setIsConnecting] = useState(false);
    const [provider, setProvider] = useState(window.ethereum);
    const [isMetaMaskInstalled, setIsMetaMaskInstalled] = useState(false);

    // as soon as started, we get provider and save
    useEffect(() => {
        setProvider(detectProvider());
        
    }, []);

    const detectProvider = () => {
        console.log("detectProvider started ");

        let provider;
        if (window.ethereum) {
            console.log("window.ethereum");
            provider = window.ethereum;
        } else if (window.web3) {
            console.log("window.web3");
            provider = window.web3.currentProvider;
        } else {
            console.warn("No Ethereum browser detected! Check out MetaMask");
        }
        console.log("provider in detectProvider : ", provider);

        return provider;
    };


    useEffect(() => {
        if (provider) {
            if (provider !== window.ethereum) {
                console.error(
                    "Not window.ethereum provider.  Do you have multiple wallets installed ?"
                );
            }else{
                setIsMetaMaskInstalled(true);
                onLoginHandler();
            }
            
        }
    }, [provider]);

    
    // when user click connect button, this func will be called
    const onLoginHandler = async () => {
        setIsConnecting(true);

        try{
            await provider.request({method: "eth_requestAccounts",});
        }catch(error){
            console.log("error :", error);
        }
        setIsConnecting(false);
        
        props.onLogin(provider);
    };


    return(
        <>
            
            <Label as='a' color='red' image onClick={onLoginHandler}>
                {isMetaMaskInstalled && (
                    <>
                        <Icon name='home' size='small'/>
                        <Label.Detail>
                            {!isConnecting && "Connect wallet"}
                            {isConnecting && "Connecting..."}
                        </Label.Detail>
                    </>
                )}
                {!isMetaMaskInstalled && (
                    <p>
                    <a href="https://metamask.io/download/">Install MetaMask</a>
                    </p>
                )} 
            </Label>
        
        </>
    );

    
};

export default ConnectButton;

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