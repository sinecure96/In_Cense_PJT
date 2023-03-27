package com.suyang.incense.api.service.perfume;

import com.suyang.incense.api.request.perfume.PerfumeReq;
import com.suyang.incense.db.entity.perfume.Perfume;

import java.util.List;

public interface PerfumeService {

    public List<Perfume> getPerfumeList(PerfumeReq perfumeReq);

    public Perfume getPerfume(Long perfumeId);
}