import React from "react";
import { Image } from "semantic-ui-react";
import { MDBAccordion, MDBAccordionItem } from 'mdb-react-ui-kit';

const Faq = ()=>{
    return (
        <>

            

                    <MDBAccordion initialActive={1}>
                        <MDBAccordionItem collapseId={1} headerTitle='받은 POAP을 다른 사람에게 보낼수 있나요'>
                            <strong>그럼요 보낼수 있습니다</strong> Opensea와 같은 NFT 거래 서비스를 이용해서 다른 사람에게 보낼수 있습니다.
                        </MDBAccordionItem>
                        <MDBAccordionItem collapseId={2} headerTitle='지갑에 POAP을 확인했는데 없어요'>
                            <strong><i className="clock icon text-primary"></i> POAP전송에 약간의 시간이 걸립니다</strong>
                            <p> 블럭체인에 데이터가 전송되고 기록되는데 상황에 따라 수십초의 시간이 걸립니다.
                            </p>
                            <p> Opensea나 다른 플랫폼에서 확인하는 경우 정보가 업데이트 되는데 추가로 시간이 걸립니다.</p>
                        </MDBAccordionItem>
                        <MDBAccordionItem collapseId={3} headerTitle='Polygon 네트워크을 사용해야 하나요?'>
                            <strong>네 polygon 네트워크를 사용하셔야 합니다.</strong> 빠르고 값싼 비용의 polygon을 이용해 주세요.
                            <br/> 지갑주소은 polygon 네트워크 주소여야 합니다. 
                            <br/> 다른 네트워크의 주소의 경우 POAP은 사라지고 찾을수 없게 됩니다. 
                        </MDBAccordionItem>
                        <MDBAccordionItem collapseId={4} headerTitle='POAP을 보내는데 Metamask 지갑이 필요한가요?'>
                            <strong><Image size='mini' src='static/for_react/images/metamask_icon.png' wrapped/> 네 매타매스크 지갑이 필요합니다</strong>
                            <p>전송하는데 매타매스크 지갑이 필요합니다.</p>
                            <p>POAP을 받는 사람은 매타매스크 지갑이 없어도 가능합니다.</p>
                            <a target="_blank" href="https://metamask.io/download" >https://metamask.io/download</a> &lt;&lt; Metamask 설치하기
                        </MDBAccordionItem>

                        <MDBAccordionItem collapseId={5} headerTitle='주소록 csv, xlsx 형식은 어떻게 되나요?'>
                            <strong><i className="address book text-primary icon"></i>주소록은 csv와 xlsx형식만 지원 됩니다.</strong>
                            <br/>
                            <br/>
                            <strong>- csv 화일</strong>
                            <br/>
                            <Image size='medium' src='static/for_react/images/csv_example.png' wrapped/>
                            <br/>
                            메모장, 워드프로세서등 원하시는 텍스트 에디터로 위에 그림과 같이 csv화일을 작성하고 <strong>.csv 확장자를</strong> 설정해서 저장하세요.
                            <br/>
                            <br/>
                            <strong>- xlsx 엑셀 화일</strong>
                            <br/>
                            <Image size='medium' src='static/for_react/images/xlsx_example.png' wrapped/>
                            <br/>
                            엑셀이나 구글시트등을 이용해서 위에 그림과 같이 화일을 작성하고 <strong>.xlsx 확장자를</strong> 설정해서 저장하세요.
                        </MDBAccordionItem>
                        <MDBAccordionItem collapseId={6} headerTitle='POAP디자인 만들기가 어려워요 쉽게 할수 있는 방법이 있나요?'>
                            <strong>디자인 만들기를 쉽게 도와주는 사이트를 이용해 보세요.</strong>
                            <p>
                                <a  target="_blank" href='https://labs.openai.com' className='text-reset'>
                                <i className="paint brush icon text-primary"></i> Dalle-e 2 
                                </a>
                            </p>
                            <p>
                                <a  target="_blank" href='https://logomakr.com/' className='text-reset'>
                                <i className="paint brush icon text-primary"></i> Logomakr.com
                                </a>
                            </p>
                            <p>
                                <a target="_blank" href='https://goodbrief.io/' className='text-reset'>
                                <i className="paint brush icon text-primary"></i> GoodBrief
                                </a>
                            </p>
                            <p>
                                <a href='https://www.logomaker.net/' className='text-reset'>
                                <i className="paint brush icon text-primary"></i> Logomaker.net
                                </a>
                            </p>
                        </MDBAccordionItem>
                    </MDBAccordion>

                    



            

        </>
    );
};

export default Faq;