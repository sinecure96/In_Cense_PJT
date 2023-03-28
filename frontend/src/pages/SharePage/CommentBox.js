import React from 'react'
import { Box } from "@mui/system";
import { TextField } from "@mui/material";
import { useState } from 'react';
import {FormControlLabel} from '@mui/material';
import { Button } from "@mui/material";
import {Checkbox} from '@mui/material';

import { RxLockClosed } from 'react-icons/rx';






function CommentBox() {
  
  const userNickname = '전태영'
  const commentWriterNickname = '전태영'

  const [replyValue, setReplyValue] = useState('')
  const onChangeReply = (e) => {
    const replyValue = e.target.value
    replyValue === null
    ? alert('답글을 입력하세요')
    : setReplyValue(replyValue)
  }
  console.log('답글내용 ==',replyValue)

  const onSubmitReply = () => {
    console.log('답글 저장')
    // 내용 담아서 쏘기!
  }

  const [isSecret, setIsSecret] = useState(0)
  const onChangeSecret = () => {
    isSecret === 0
    ? setIsSecret(1)
    : setIsSecret(0)

    console.log('비밀댓글 여부 변경')
  }
  console.log('답글비밀여부==',isSecret)

  const [showPostReply, setShowPostReply] = useState(false)
  const onClickPostReply = () => {
    showPostReply === false
    ? setShowPostReply(true)
    : setShowPostReply(false)
  }
  
  const [isForEdit, setIsForEdit] = useState(false)
  const onEditcomment = () => {
    setIsForEdit(true)
  }

  const onDeleteComment = () => {
    console.log('delete comment')
  }

  const commentIsSecret = false

  if (commentIsSecret === true) {
    return (
      <div>
      <Box sx={{width:'100%',height:'8rem',marginLeft:'1rem', display:'flex',flexDirection:'column', borderTop:'1px solid lightgrey',justifyContent:'center'}}>
        <div style={{margin:'0.5rem',display:'flex',flexDirection:'row'}}>
          <p style={{marginTop:'1rem',marginRight:'0.5rem'}}><RxLockClosed/></p>          <p style={{marginTop:'1rem'}}>비밀입니다.</p>
        </div>
      </Box>
      <Box sx={{backgroundColor:'#F3F3F3',width:'100%',height:'8rem',marginLeft:'1rem', display:'flex',flexDirection:'row',borderTop:'1px solid lightgrey'}}>
        <Box sx={{width:'5%',display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center'}}>
            <img src= '/assets/icons/reply.svg' alt='reply'/>
        </Box>
        <Box sx={{width:'95%',display:'flex',flexDirection:'column',justifyContent:'center'}}> 
          <div style={{margin:'0.5rem',display:'flex',flexDirection:'row'}}>
            <p style={{marginTop:'1rem',marginRight:'0.5rem'}}><RxLockClosed/></p>
            <p style={{marginTop:'1rem'}}>이것도 비밀</p>
          </div>
        </Box>   
      </Box>
      {showPostReply === true      
      ? <Box sx={{backgroundColor:'#F3F3F3',width:'100%',height:'8rem',marginLeft:'1rem', display:'flex',flexDirection:'row',borderTop:'1px solid lightgrey'}}>
          <Box sx={{width:'5%',display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center'}}>
            <img src= '/assets/icons/reply.svg' alt='reply'/>
          </Box>
          <Box sx={{width:'95%'}}>
            <TextField fullWidth multiline rows={2} label="답글을 입력하세요" id="commentfield" size='small' sx={{marginTop:'0.5rem', width:'95%',backgroundColor:'white',borderRadius:'5px'}}
            onChange={onChangeReply}/>
            <Box sx={{width:'95%',display:'flex',flexDirection:'row',justifyContent:'flex-end',marginTop:'0.5rem'}}>
              <FormControlLabel control={<Checkbox size='small' />} label="비밀답글" sx={{marginRight:'3rem',fontSize:'0.8rem'}} onChange={onChangeSecret}/>
              <Button sx={{width:'4rem',height:'2rem', fontWeight:'bold',fontSize:'0.9rem',top:'0.2rem'}} variant='contained' component="label"
                onClick={onSubmitReply} size='small'> 
                저장
              </Button>
            </Box>
          </Box>
        </Box>
      :<></>}
      </div>
    )
  } else {

  return (
    <div>
    <Box sx={{width:'100%',height:'8rem',marginLeft:'1rem', display:'flex',flexDirection:'column', borderTop:'1px solid lightgrey'}}>
      <div style={{margin:'0.5rem'}}>
        
        
        <Box sx={{display:'flex',flexDirection:'row',justifyContent:'space-between'}}>  
        <p style={{fontWeight:'bold',fontSize:'1.1rem'}}>전태영</p>
        {userNickname === commentWriterNickname
        ?<Box>
          <img
          src="/assets/icons/edit.svg"
          alt="modify"
          // style={{ position: "absolute", right: "0" }}
          style={{marginRight:'0.5rem',cursor:'pointer'}}
          onClick={onEditcomment}
          />
          <img
          src="/assets/icons/delete.svg"
          alt="modify"
          style={{width:'18px',height:'18px',marginBottom:'1px',cursor:'pointer'}}
          onClick={onDeleteComment}
          />
          </Box>
        :<></> }
        
        </Box>
        
        <p style={{marginTop:'1rem'}}>이건 댓글내용 -------</p>
        <p style={{marginTop:'0.5rem',fontSize:'0.7rem', color:'grey'}}>2023.03.22 12:52</p>
        <p onClick={onClickPostReply} style={{marginTop:'0.5rem',fontSize:'0.9rem',cursor:'pointer'}}>답글 달기</p>
      </div>
    </Box>
    <Box sx={{backgroundColor:'#F3F3F3',width:'100%',height:'8rem',marginLeft:'1rem', display:'flex',flexDirection:'row',borderTop:'1px solid lightgrey'}}>
      <Box sx={{width:'5%',display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center'}}>
          <img src= '/assets/icons/reply.svg' alt='reply'/>
      </Box>
      <Box sx={{width:'95%'}}> 
        <div style={{margin:'0.5rem'}}>
          <Box sx={{display:'flex',flexDirection:'row',justifyContent:'space-between'}}>
          <p style={{fontWeight:'bold',fontSize:'1.1rem'}}>전태영</p>
          {userNickname === commentWriterNickname
          ?<Box>
            <img
            src="/assets/icons/edit.svg"
            alt="modify"
            // style={{ position: "absolute", right: "0" }}
            style={{marginRight:'0.5rem',cursor:'pointer'}}
            onClick={onEditcomment}
            />
            <img
            src="/assets/icons/delete.svg"
            alt="modify"
            style={{width:'18px',height:'18px',marginBottom:'1px',cursor:'pointer'}}
            onClick={onDeleteComment}
            />
            </Box>
          :<></> }
          
          </Box>
          
          <p style={{marginTop:'1rem'}}>이건 답글내용 -------</p>
          <p style={{marginTop:'0.5rem',fontSize:'0.7rem', color:'grey'}}>2023.03.22 12:52</p>
          <p onClick={onClickPostReply} style={{marginTop:'0.5rem',fontSize:'0.9rem',cursor:'pointer'}}>답글 달기</p>
        </div>
      </Box>   
    </Box>
    {showPostReply === true      
    ? <Box sx={{backgroundColor:'#F3F3F3',width:'100%',height:'8rem',marginLeft:'1rem', display:'flex',flexDirection:'row',borderTop:'1px solid lightgrey'}}>
        <Box sx={{width:'5%',display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center'}}>
          <img src= '/assets/icons/reply.svg' alt='reply'/>
        </Box>
        <Box sx={{width:'95%'}}>
          <TextField fullWidth multiline rows={2} label="답글을 입력하세요" id="commentfield" size='small' sx={{marginTop:'0.5rem', width:'95%',backgroundColor:'white',borderRadius:'5px'}}
          onChange={onChangeReply}/>
          <Box sx={{width:'95%',display:'flex',flexDirection:'row',justifyContent:'flex-end',marginTop:'0.5rem'}}>
            <FormControlLabel control={<Checkbox size='small' />} label="비밀답글" sx={{marginRight:'3rem',fontSize:'0.8rem'}} onChange={onChangeSecret}/>
            <Button sx={{width:'4rem',height:'2rem', fontWeight:'bold',fontSize:'0.9rem',top:'0.2rem'}} variant='contained' component="label"
              onClick={onSubmitReply} size='small'> 
              저장
            </Button>
          </Box>
        </Box>
      </Box>
    :<></>}
    </div>
  )}
}

export default CommentBox