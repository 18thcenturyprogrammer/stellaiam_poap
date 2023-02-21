
async function main(){
    // attachGroundSBTmintEventListener();

    const eventsData = await checkClaimEvent();

    makeServerPay(eventsData);


    while(true){
        const oneSecond = 1000;
        const oneMinuate = 60;
        const oneHour = 60;
        await sleep(oneSecond*oneMinuate*10);
        console.log("now :",Date.now());
        // attachGroundSBTmintEventListener();
    };
}


const checkClaimEvent = async ()=>{

    require('dotenv').config();
    // console.log(process.env);

    const { ethers, BigNumber } = require("ethers");

    // const contractAddress = process.env.STELLAIAM_CONTRACT_ADDRESS;
    const contractAddress = process.env.STELLAIAM_POAP_CONTRACT_ADDRESS;

    console.log("contractAddress :",contractAddress);

    const abi = process.env.ABI;    

    // const providerUrl = process.env.ALCHEMY_WEB_SOCKET;
    const providerUrl = process.env.ALCHEMY_WEB_SOCKET;

    const provider = new ethers.providers.WebSocketProvider(providerUrl);
    const stellaiamPoapContract = new ethers.Contract(contractAddress,abi,provider);


    // ethers event filter 
    // ref) https://ethereum.stackexchange.com/questions/91966/get-number-of-all-the-past-events-using-ethers-v5
    // ref) https://docs.ethers.org/v5/api/contract/example/#erc20-meta-events

    // const filter = await stellaiamPoapContract.filters.paidPoapClaim(null,82, 1);
    // const filter = await stellaiamPoapContract.filters.paidPoapClaim("0x94f2F7dEef8b5778b0Ad706cD9d6d19aC11a3f04",82, 1);
    // const filter = stellaiamPoapContract.filters.paidPoapClaim("0x94f2F7dEef8b5778b0Ad706cD9d6d19aC11a3f04",82, 5);
    // const filter = stellaiamPoapContract.filters.paidPoapClaim("0x94f2F7dEef8b5778b0Ad706cD9d6d19aC11a3f04");
    // const filter = await stellaiamPoapContract.filters.paidPoapClaim(null,112);
    const filter = await stellaiamPoapContract.filters.paidPoapClaim();
    

    // basic format is : queryFilter(filter, _startBlock, _endBlock)
    // 60000 is about 1 day before

    // const events = await stellaiamPoapContract.queryFilter(filter, -10, "latest");
    // const events = await stellaiamPoapContract.queryFilter(filter, -1, "latest");

    // get events which happened in one last day
    // const events = await stellaiamPoapContract.queryFilter(filter, -60000, "latest");
    const events = await stellaiamPoapContract.queryFilter(filter, -10000, "latest");
    
    console.log("events : ", events);
    
    // parce event log 
    // ref) https://github.com/ethers-io/ethers.js/issues/487
    let iface = new ethers.utils.Interface(abi);

    let readableEvents = events.map((event) => iface.parseLog(event))
    
    
    return readableEvents;
};

const makeServerPay = (eventsData)=>{

    
    console.log("process.env.PASSWORD : ", process.env.PASSWORD);
    
    // console.log("eventsData : ", eventsData);
    // console.log("eventsData[0].args : ", eventsData[0].args);
    // console.log("eventsData[0].args.whoPaid : ", eventsData[0].args.whoPaid);
    // console.log("Number(eventsData[0].args.claimId) : ", Number(eventsData[0].args.claimId));
    // console.log("eventsData[0].args.howMany : ", eventsData[0].args.howMany);
    
    for (const [key, value] of Object.entries(eventsData)) {
        console.log("key == ",key);
        
        if(key ==0 || key ==1){
            console.log(`${key}: ${value.args.whoPaid}`);
            console.log(`${key}: ${Number(value.args.claimId)}`);
            console.log(`${key}: ${Number(value.args.howMany)}`);
            
            var axios = require('axios');


            axios.post(process.env.WEBSITE+"api/paid_direct_poap_claim/", {
                password: process.env.PASSWORD,
                whoPaid: value.args.whoPaid,
                claimId: Number(value.args.claimId),
                howMany: Number(value.args.howMany)
            }).then((response)=>{
                // console.log("response obj : ");
                // console.dir(response);

                if(response.status == 200){
                    console.log("response.data",response.data);

                    
                }else{
                    throw Error("Failed communication with server for saving content");
                }
            }).catch(function (response) {
                //handle error
                console.log(response);
            });
        
        }


        

        
    }
};


const attachGroundSBTmintEventListener = ()=>{
    require('dotenv').config();
    // console.log(process.env);

    const { ethers, BigNumber } = require("ethers");

    const contractAddress = process.env.STELLAIAM_CONTRACT_ADDRESS;

    console.log("contractAddress :",contractAddress);

    const abi = process.env.ABI;    

    const providerUrl = process.env.ALCHEMY_WEB_SOCKET;

    const provider = new ethers.providers.WebSocketProvider(providerUrl);
    const stellaiamNftContract = new ethers.Contract(contractAddress,abi,provider);

    try {
        // getting data from event 
        // parameters are same as emit signature
        stellaiamNftContract.on("groundSBTminted", async (whose, cryptedData, exposedData, institutionName, instituionNameLabel, at, additionalData) => {
            // user minted groundSBT , now we make stellaSBT
            
            // unindexed data will be shown as same as passed
            // long indexed data will be hashed 
            // short indexed data will be show as same as passed

            console.log("whose :", whose);
            console.log("cryptedData :", cryptedData);
            console.log("exposedData :", exposedData);
            console.log("institutionName :", institutionName);
            console.log("instituionNameLabel :", instituionNameLabel);
            console.log("at :", at);



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// this is about getting unindexed data from event             
            // additional data is in JSON format, and 'data' has unindexed data in hex  
            // console.log("additionalData :", additionalData);

            // getting data from event 
            // https://ethereum.stackexchange.com/a/87656
            // https://web3js.readthedocs.io/en/v1.2.11/web3-eth-abi.html#decodeparameters


            // const Web3 = require('web3');
            // const web3 = new Web3();

            // // const typesArray = [
            // //     {type: 'address', name: '_whose'}, 
            // //     {type: 'string', name: '_cryptedData'},
            // //     {type: 'string', name: '_exposedData'},
            // //     {type: 'string', name: '_instituionName'},
            // //     {type: 'uint256', name: '_at'}
            // // ];

            // const typesArray = [
            //     'string', 'string'
            // ];

            // const data = additionalData.data;

            // const decodedParameters = web3.eth.abi.decodeParameters(typesArray, data);

            // console.log(JSON.stringify(decodedParameters, null, 4));
            
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////





           
            
            // const cleanedExposedDate = JSON.stringify(exposedData); 
            // const jsonExposedData = JSON.parse(cleanedExposedDate);

            const jsonExposedData = JSON.parse(exposedData);

            

            await createMintImg(whose, jsonExposedData, instituionNameLabel);

            const imgCid = await pinImg(whose,instituionNameLabel);

            if (imgCid == null){
                // there is a problem while we upload image to pinata ipfs 
                return null;
            }else{
                const metaDataCid = await pinMetaData(imgCid,whose,jsonExposedData,instituionNameLabel);

                if(metaDataCid == null){
                    // there is a problem while we upload metadata to pinata ipfs 
                    return null;
                }else{
                    const uri = "https://gateway.pinata.cloud/ipfs/"+metaDataCid;
                    mintStellaSBT(whose, cryptedData, exposedData, instituionNameLabel, uri);
                }
            }

        });
        
    } catch (error) {
        console.log("error raised");
        console.dir(error);
    }
};


function sleep(ms){
    return new Promise(resolve => setTimeout(resolve,ms));
}

// divide string into n length string elements
// ref) https://stackoverflow.com/a/14349616
function chunkString (str, len) {
    const size = Math.ceil(str.length/len)
    const r = Array(size)
    let offset = 0
    
    for (let i = 0; i < size; i++) {
      r[i] = str.substr(offset, len)
      offset += len
    }
    
    return r
}



// pin image to pinata 
// pinata docs ref) https://docs.pinata.cloud/pinata-api/pinning/pin-file-or-directory
const pinImg = async (whose, institutionName)=>{
    const axios = require('axios')
    const FormData = require('form-data')
    const fs = require('fs')

    const formData = new FormData();
    const src = `../public/imgs/users/${whose}.png`;
    
    const file = fs.createReadStream(src)
    formData.append('file', file)

    const metadata = JSON.stringify({
        name: whose+"_"+institutionName,
        keyValues: {
            ownerAddress: whose,
            institutionName : institutionName, 
            imgIpfsCreated : Date.now()
        }
    });
    formData.append('pinataMetadata', metadata);

    const options = JSON.stringify({
        cidVersion: 0,
    })
    formData.append('pinataOptions', options);


    try{
        const res = await axios.post("https://api.pinata.cloud/pinning/pinFileToIPFS", formData, {
          maxBodyLength: "Infinity",
          headers: {
            'Content-Type': `multipart/form-data; boundary=${formData._boundary}`,
            'Authorization': 'Bearer '+process.env.PINATA_JWT_TOKEN
          }
        });
        console.log("pinata img pin res.data = ",res.data);

        return res.data.IpfsHash;
        
    } catch (error) {
        console.log("error while pinata = ",error);

        return null;
    }


};

const pinMetaData = async (imgCid, whose, exposedData, institutionName)=>{
    var axios = require('axios');

    // const partAddress = whose.substring(whose.length-4,whose.length); 
    const partAddress = smartTrim(whose,8);

    var sbtData ="Soul bount token data\n";
    Object.entries(exposedData).forEach(([k,v])=>{
        sbtData += k;
        sbtData += " : ";
        sbtData += v+"\n";
    });

    var data = JSON.stringify({
    "pinataOptions": {
        "cidVersion": 1
    },
    "pinataMetadata": {
        name: whose+"_"+institutionName,
        keyValues: {
            ownerAddress: whose,
            institutionName : institutionName, 
            imgIpfsCreated : Date.now()
        }
    },
    "pinataContent": {
        "image": "https://gateway.pinata.cloud/ipfs/"+imgCid,
        "name": partAddress +` stellaiam SBT (${institutionName})`,
        "description": `This is SBT soul bount token which is issued by Stellaiam. \n User data is get from ${institutionName} Oauth.\n ${sbtData}`
    }
    });

    var config = {
    method: 'post',
    url: 'https://api.pinata.cloud/pinning/pinJSONToIPFS',
    headers: { 
        'Content-Type': 'application/json', 
        'Authorization': `Bearer ${process.env.PINATA_JWT_TOKEN}`
    },
    data : data
    };

    try{
        const res = await axios(config);

        console.log("pinata json pin res.data = ",res.data);

        return res.data.IpfsHash
    } catch (error) {
        console.log("error while pinata = ",error);
        return null;
    }
};

const mintStellaSBT = async (whose, cryptedData, exposedData, institutionName, uri)=>{
    
    console.log("mintStellaSBT is called");

    try {
        const { ethers, BigNumber } = require("ethers");

        const abi = process.env.ABI;
        const stellaiamContractAddress = process.env.STELLAIAM_CONTRACT_ADDRESS;

        const provider = new ethers.providers.JsonRpcProvider(process.env.ALCHEMY_MUMBAI_HTTP);
        
        const stellaiamNftContract = new ethers.Contract(stellaiamContractAddress,abi,provider);

        const wallet = new ethers.Wallet(process.env.PRIV_KEY);
        
        const connectedWallet = wallet.connect(provider);

        
        const gasData = await provider.getFeeData();

        // 'replacement fee too low' error kept being raised, so i had to jack up the gas

        // if i follow eip 1559, i can't override gasprice option
        // maxFeePerGas must be higher than maxPriorityFeePerGas
        const mulMaxFeePerGas = gasData.maxFeePerGas.mul(BigNumber.from(50));
        const mulMaxPriorityFeePerGas = gasData.maxPriorityFeePerGas.mul(BigNumber.from(40));
        

        // normal gasLimit is 21000 , but not worked ,so i changed it to this
        const options = {
            value: 0,
            gasLimit:ethers.utils.hexlify(1000000),
            maxFeePerGas:mulMaxFeePerGas,
            maxPriorityFeePerGas:mulMaxPriorityFeePerGas,
            nonce: await provider.getTransactionCount(process.env.WALLET_ADDRESS)
        };
        
        // send transaction with value
        // ref) https://vsupalov.com/ethers-call-payable-solidity-function/
        const result = await stellaiamNftContract.connect(connectedWallet).mintByOwner(whose,1,cryptedData,exposedData,institutionName,uri, options);
        
        const txReceipt = await result.wait();

        console.log("txReceipt : ", txReceipt);
        console.dir(txReceipt);

        if(txReceipt.blockNumber){
            console.log("stella SBT minted all right");
        }


    } catch (error) {
        console.log("failed to mint stella SBT :", error);
        console.dir(error);
    }
};


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


main();


