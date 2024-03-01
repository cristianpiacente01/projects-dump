package net.cpbackend.service;

import org.springframework.stereotype.Service;
import net.cpbackend.model.Stabilimento;
import net.cpbackend.repository.IStabilimentoRepository;

@Service
public class StabilimentoService extends BaseCrudService<Stabilimento, IStabilimentoRepository> {
}