import React from "react";
import { useNavigate } from "react-router-dom";

import { Image } from "semantic-ui-react";

import {
    MDBCard,
    MDBCardBody,
    MDBCardTitle,
    MDBCardText,
    MDBCardHeader,
    MDBCardFooter,
    MDBBtn
  } from 'mdb-react-ui-kit';




const PriceCards = ()=>{

    const navigate = useNavigate();

    const onClickSendSingle = ()=>{
        console.log("onClickSendSingle called");

        navigate('/send_poap_direct');
    };
    const onClickSendMultiple = ()=>{
        console.log("onClickSendMultipl called");

        navigate('/send_poap_direct');
    };
    const onClickSendLink = ()=>{
        console.log("onClickSendLink called");

        navigate('/send_poap_non_direct');
    };

    return (
        <>

            <div id="PriceCards" className="ui three column grid">
                <div className="column">
                    <div className="ui">

                    <MDBCard alignment='center'>
                    <MDBCardHeader>Featured</MDBCardHeader>
                    <MDBCardBody>
                        <MDBCardTitle><i className="child icon text-primary"></i> 1개 직접보내기</MDBCardTitle>
                        <MDBCardText><p>하나의 주소로 직접 POAP 보내기</p><p>간단하게 주소, POAP디자인 만으로 바로보내기</p></MDBCardText>
                        <MDBBtn onClick={onClickSendSingle} >Go</MDBBtn>
                    </MDBCardBody>
                    <MDBCardFooter className='text-muted'>가격: 2 Matic</MDBCardFooter>
                    </MDBCard>

                    </div>
                </div>

                <div className="column">
                    <div className="ui">
                    
                    <MDBCard alignment='center'>
                    <MDBCardHeader>Featured</MDBCardHeader>
                    <MDBCardBody>
                        <MDBCardTitle><i className="users icon text-primary"></i>여러 사람에게 보내기</MDBCardTitle>
                        <MDBCardText><p>주소가 들어 있는 주소록을 이용해서 보냅니다</p><p>csv, xlsx 엑셀파일, POAP디자인이 있다면 쉽게 많은 사람에게 보낼수 있어요</p></MDBCardText>
                        <MDBBtn onClick={onClickSendMultiple} >Go</MDBBtn>
                    </MDBCardBody>
                    <MDBCardFooter className='text-muted'>1개당 1.5 Matic</MDBCardFooter>
                    </MDBCard>

                    </div>
                </div>

                <div className="column">
                    <div className="ui">
                    
                    <MDBCard alignment='center'>
                    <MDBCardHeader>Featured</MDBCardHeader>
                    <MDBCardBody>
                        <MDBCardTitle><i className="linkify icon text-primary"></i> 링크 만들기</MDBCardTitle>
                        <MDBCardText><p>POAP을 받을수 있는 링크,QR코드 만들기</p><p>인증코드와 POAP디자인으로 링크를 만들면</p><p>다른 사람들이 받을수 있어요</p></MDBCardText>
                        <MDBBtn onClick={onClickSendLink} >Go</MDBBtn>
                    </MDBCardBody>
                    <MDBCardFooter className='text-muted'>1개당 1.5 Matic</MDBCardFooter>
                    </MDBCard>

                    </div>
                </div>


            </div>

        </>
    );
};

export default PriceCards;