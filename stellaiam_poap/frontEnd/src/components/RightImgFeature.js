import React from "react";

import { Image } from "semantic-ui-react";
import { MDBTypography } from "mdb-react-ui-kit";

const RightImgFeature = ()=>{
    return (
        <>

            <div id="RightImgFeature" className="ui two column grid">
                <div id="firstCol" className="column">
                    <div className="ui">
                    <h2><MDBTypography className="text-primary" tag='strong'>POAP</MDBTypography> 를 왜 사용하나요?</h2>
                    <h4><i className="minus icon text-primary"></i>&nbsp;사용자는 POAP를 통해 크립토 세상에서의 아이덴티티를 얻을수 있습니다</h4>
                    <br />
                    <h4><i className="minus icon text-primary"></i>&nbsp;POAP는 블럭체인에 안전하게 보관됩니다</h4>
                    <br />
                    <h4><i className="minus icon text-primary"></i>&nbsp;사용자는 POAP를 통해 손쉽게 다른 사람에게 본인의 정체성을 보여줄수 있습니다</h4>
                    </div>
                </div>
                <div id="firstCol" className="column">
                    <div className="ui">
                    <Image size='large' src='static/for_react/images/why2.png' wrapped/>
                    </div>
                </div>
            
            </div>

        </>
    );
};

export default RightImgFeature;