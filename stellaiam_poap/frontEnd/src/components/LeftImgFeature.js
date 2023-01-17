import React from "react";

import { Image } from "semantic-ui-react";
import { MDBTypography } from "mdb-react-ui-kit";

const LeftImgFeature = ()=>{
    return (
        <>

            <div id="LeftImgFeature" className="ui two column grid">
                <div id="firstCol" className="column">
                    <div className="ui">
                    <Image size='large' src='static/for_react/images/what.png' wrapped/>
                    </div>
                </div>
                <div id="secondCol" className="column">
                    <div className="ui">
                    <h2><MDBTypography className="text-primary" tag='strong'>POAP</MDBTypography> 는 무엇인가요?</h2>
                    <h4><i className="quote left icon text-primary"></i>&nbsp;&nbsp;&nbsp;Proof of Attendance Protocol 는 NFT의 하나로 특정한 이벤트에 참석하거나 특정한 과정을 완료 했을때 받는 토큰 입니다</h4>
                    <br />
                    <h4>이벤트의 기념품일수도 있고 과정을 이수한 증명서가 될수도 있습니다 &nbsp;&nbsp;&nbsp;<i className="quote right icon text-primary"></i></h4>
                    </div>
                </div>
            </div>

        </>
    );
};

export default LeftImgFeature;