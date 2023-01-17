import React from "react";

import { Image } from "semantic-ui-react";
import { MDBTypography } from "mdb-react-ui-kit";

const LeftImgFeature2 = ()=>{
    return (
        <>

            <div id="LeftImgFeature2" className="ui two column grid">
                <div id="firstCol" className="column">
                    <div className="ui">
                    <Image size='large' src='static/for_react/images/how2.png' wrapped/>
                    </div>
                </div>
                <div id="secondCol" className="column">
                    <div className="ui">
                    <h2><MDBTypography className="text-primary" tag='strong'>POAP</MDBTypography> 를 어떻게 사용할까요?</h2>
                    <h4><i className="minus icon text-primary"></i>&nbsp;참가 기념품 : 힙합 콘서트, 미술 전시회, 개발자 세미나, 수학여행등 기억으로 남기고 싶은 모든 이벤트</h4>
                    <br />
                    <h4><i className="minus icon text-primary"></i>&nbsp;과정이수 증명 : 요리교실, 주짓수 승급, 소물리에 과정,  수업과정, 각종 자격증등 실력을 보여주고 자랑할 모든 과정</h4>
                    <br />
                    <h4><i className="minus icon text-primary"></i>&nbsp;기념품이나 증명서가 아니더라도 친구나 가족에게 선물로 줄수도 있습니다</h4>
                    </div>
                </div>
            </div>

        </>
    );
};

export default LeftImgFeature2;