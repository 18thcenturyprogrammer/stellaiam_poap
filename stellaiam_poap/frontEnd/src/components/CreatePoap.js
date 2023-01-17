import React, {useEffect, useState} from "react";

import { useNavigate } from "react-router-dom";

import { Image } from "semantic-ui-react";
import { MDBTypography } from "mdb-react-ui-kit";

import Menu from "./Menu";
import Footer from "./Footer";




const CreatePoap = ()=>{

    const [hasMetamask, setHasMetamask] = useState(false);

    // as soon as started, we get provider and save
    useEffect(() => {
        detectProvider();
        
    }, []);

    const detectProvider = () => {
        console.log("detectProvider started ");

        let provider;
        if (window.ethereum) {
            console.log("window.ethereum");
            setHasMetamask(true);
        } else if (window.web3) {
            console.log("window.web3");
            setHasMetamask(false);
        } else {
            console.warn("No Ethereum browser detected! Check out MetaMask");
            setHasMetamask(false);
        }
    };


    const navigate = useNavigate();

    const GoSendPoapDirectPage = ()=>{
        console.log("GoSendPoapDirectPage is called");
    
        navigate("/send_poap_direct");
    };
    
    const GoSendPoapNonDirectPage = ()=>{
        console.log("GoSendPoapNonDirectPage is called");
            
        navigate("/send_poap_non_direct");
    };

    const GoInstallMetamaskPage = ()=>{
        console.log("GoInstallMetamaskPage is called");
            
        window.open('https://metamask.io/download', '_blank', 'noreferrer');
    };

    

    const getContent = (has)=>{

        console.log("has : ", has);

        if(has){
            return (
                <>

                <div className='p-5 text-center bg-light'>
                    <h1 className='mb-3'><i className="paper plane icon text-primary"></i>&nbsp;받는이에게 POAP 바로 보내기</h1>
                    <h5 className='mb-3'>POAP를 만들어서 받는이에게 바로 보냅니다</h5>
                    <h5 className='mb-3'>준비물 : 받는이의 지갑주소, 디자인 이미지, 메타매스크지갑</h5>
                    <h5 className='mb-3'>받는 사람들이 많은 경우 지갑주소들이 들어있는 csv파일이 필요합니다</h5>
                    <button className="ui primary button" onClick={GoSendPoapDirectPage}>
                    Go
                    </button>
                </div>

                <h2 className="ui horizontal divider header">
                    
                    &nbsp; OR &nbsp;
                    
                </h2>

                <div className='p-5 text-center bg-light'>
                    <h1 className='mb-3'><i className="linkify icon text-primary"></i>&nbsp;POAP 받을수 있는 링크 만들기</h1>
                    <h5 className='mb-3'>POAP를 만들고 받는이들이 POAP를 받을수 있는 링크를 만듭니다</h5>
                    <h5 className='mb-3'>준비물: 디자인 이미지, 메타매스크지갑</h5>
                    <button className="ui primary button" onClick={GoSendPoapNonDirectPage}>
                    Go
                    </button>
                </div>

                </>
            );
        }else{
            return(
                <>
                
                <div className='p-5 text-center bg-light'>
                    <h1 className='mb-3'><i className="exclamation circle icon text-warning"></i>&nbsp;설치된 Metamask 지갑이 없습니다</h1>
                    <h5 className='mb-3'>POAP를 만들기 위해서는 Metamask 지갑이 필요합니다</h5>
                    <button className="ui primary button" onClick={GoInstallMetamaskPage}>
                    Metamask 페이지로 이동
                    </button>
                </div>

                </>
            );
        }
    };

    return (
        <>

            <Menu updateProvider={()=>{}} updateCurrentAccount={()=>{}} />
            <div id="CreateProp">
                {getContent(hasMetamask)}
            </div>

            <Footer />   

        </>
    );
};

export default CreatePoap;