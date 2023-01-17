import React from "react";

import { MDBFooter, MDBContainer, MDBRow, MDBCol, MDBIcon } from 'mdb-react-ui-kit';

const Footer = ()=>{
    return (
        <>
            <div id="Footer">
            <MDBFooter bgColor='primary' className='text-white text-center text-lg-start'>
                <section className='d-flex justify-content-center justify-content-lg-between p-4 border-bottom'>
                    <div className='me-5 d-none d-lg-block'>
                    <span>Get connected with us on social networks:</span>
                    </div>

                    <div>
                    <a href='' className='me-4 text-reset'>
                        <MDBIcon color='light' fab icon='facebook-f' />
                    </a>
                    <a href='' className='me-4 text-reset'>
                        <MDBIcon color='light' fab icon='twitter' />
                    </a>
                    <a href='' className='me-4 text-reset'>
                        <MDBIcon color='light' fab icon='google' />
                    </a>
                    <a href='' className='me-4 text-reset'>
                        <MDBIcon color='light' fab icon='instagram' />
                    </a>
                    <a href='' className='me-4 text-reset'>
                        <MDBIcon color='light' fab icon='linkedin' />
                    </a>
                    <a href='' className='me-4 text-reset'>
                        <MDBIcon color='light' fab icon='github' />
                    </a>
                    </div>
                </section>

                <section className=''>
                    <MDBContainer className='text-center text-md-start mt-5'>
                    <MDBRow className='mt-3'>
                        <MDBCol md='3' lg='4' xl='3' className='mx-auto mb-4'>
                        <h6 className='text-uppercase fw-bold mb-4'>
                            <MDBIcon color='light' icon='gem' className='me-3' />
                            Stellaiam
                        </h6>
                        <p>
                            스텔라 아임은 블럭체인을 기반으로 하며 사용자들이 쉽게 POAP, SBT&#40;soul bound token&#41; 발행, 관리하도록 돕는 플랫폼을 제공합니다
                        </p>
                        </MDBCol>

                        <MDBCol md='2' lg='2' xl='2' className='mx-auto mb-4'>
                        <h6 className='text-uppercase fw-bold mb-4'>Products</h6>
                        <p>
                            <a href='#!' className='text-reset'>
                            Angular
                            </a>
                        </p>
                        <p>
                            <a href='#!' className='text-reset'>
                            React
                            </a>
                        </p>
                        <p>
                            <a href='#!' className='text-reset'>
                            Vue
                            </a>
                        </p>
                        <p>
                            <a href='#!' className='text-reset'>
                            Laravel
                            </a>
                        </p>
                        </MDBCol>

                        <MDBCol md='3' lg='2' xl='2' className='mx-auto mb-4'>
                        <h6 className='text-uppercase fw-bold mb-4'>Useful links</h6>
                        <p>
                            <a href='#!' className='text-reset'>
                            Pricing
                            </a>
                        </p>
                        <p>
                            <a href='#!' className='text-reset'>
                            Settings
                            </a>
                        </p>
                        <p>
                            <a href='#!' className='text-reset'>
                            Orders
                            </a>
                        </p>
                        <p>
                            <a href='#!' className='text-reset'>
                            Help
                            </a>
                        </p>
                        </MDBCol>

                        <MDBCol md='4' lg='3' xl='3' className='mx-auto mb-md-0 mb-4'>
                        <h6 className='text-uppercase fw-bold mb-4'>Contact</h6>
                        <p>
                            <MDBIcon color='light' icon='home' className='me-2' />
                            Portland, OR, US
                        </p>
                        <p>
                            <MDBIcon color='light' icon='envelope' className='me-3' />
                            18thcenturyprogrammer@gmail.com
                        </p>
                        <p>
                            <MDBIcon color='light' icon='phone' className='me-3' /> + 01 234 567 88
                        </p>
                        <p>
                            <MDBIcon color='light' icon='print' className='me-3' /> + 01 234 567 89
                        </p>
                        </MDBCol>
                    </MDBRow>
                    </MDBContainer>
                </section>

                <div className='text-center p-4' style={{ backgroundColor: 'rgba(0, 0, 0, 0.05)' }}>
                    © 2023 Copyright:
                    <a className='text-reset fw-bold' href=''>
                    &nbsp;Stellaiam
                    </a>
                </div>
            </MDBFooter>
            </div>
            




        </>
    );
};

export default Footer;