import React from "react";

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
    return (
        <>

            <div id="PriceCards" className="ui three column grid">
                <div className="column">
                    <div className="ui">

                    <MDBCard alignment='center'>
                    <MDBCardHeader>Featured</MDBCardHeader>
                    <MDBCardBody>
                        <MDBCardTitle>Special title treatment</MDBCardTitle>
                        <MDBCardText>With supporting text below as a natural lead-in to additional content.</MDBCardText>
                        <MDBBtn href='#'>Button</MDBBtn>
                    </MDBCardBody>
                    <MDBCardFooter className='text-muted'>2 days ago</MDBCardFooter>
                    </MDBCard>

                    </div>
                </div>

                <div className="column">
                    <div className="ui">
                    
                    <MDBCard alignment='center'>
                    <MDBCardHeader>Featured</MDBCardHeader>
                    <MDBCardBody>
                        <MDBCardTitle>Special title treatment</MDBCardTitle>
                        <MDBCardText>With supporting text below as a natural lead-in to additional content.</MDBCardText>
                        <MDBBtn href='#'>Button</MDBBtn>
                    </MDBCardBody>
                    <MDBCardFooter className='text-muted'>2 days ago</MDBCardFooter>
                    </MDBCard>

                    </div>
                </div>

                <div className="column">
                    <div className="ui">

                    <MDBCard alignment='center'>
                    <MDBCardHeader>Featured</MDBCardHeader>
                    <MDBCardBody>
                        <MDBCardTitle>Special title treatment</MDBCardTitle>
                        <MDBCardText>With supporting text below as a natural lead-in to additional content.</MDBCardText>
                        <MDBBtn href='#'>Button</MDBBtn>
                    </MDBCardBody>
                    <MDBCardFooter className='text-muted'>2 days ago</MDBCardFooter>
                    </MDBCard>

                    </div>
                </div>

            </div>

        </>
    );
};

export default PriceCards;